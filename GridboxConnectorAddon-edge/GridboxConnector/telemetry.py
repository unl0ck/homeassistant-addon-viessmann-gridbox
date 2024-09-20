import logging
import requests
import uuid
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler

class Telemetry:
    def __init__(self, collector_endpoint, service_name):
        self.service_instance_id = str(uuid.uuid4())
        self.resource = Resource(attributes={
            ResourceAttributes.SERVICE_NAME: service_name,
            ResourceAttributes.SERVICE_INSTANCE_ID: self.service_instance_id
        })

        # Instrument the logging module
        LoggingInstrumentor().instrument(set_logging_format=True, log_level=logging.DEBUG)
        # Set up logging
        logging.basicConfig(level=logging.DEBUG)

        # Set up the tracer provider and exporter
        trace.set_tracer_provider(TracerProvider(resource=self.resource))
        self.tracer = trace.get_tracer(__name__)

        # Set up the OTLP exporter
        otlp_exporter = OTLPSpanExporter(endpoint=collector_endpoint, insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        # Instrument the requests library
        RequestsInstrumentor().instrument()

        # Create and set the logger provider
        logger_provider = LoggerProvider(resource=self.resource)
        set_logger_provider(logger_provider)

        exporter = OTLPLogExporter(endpoint=collector_endpoint, insecure=True)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)

        # Attach OTLP handler to root logger
        logging.getLogger().addHandler(handler)
        self.logger = logging.getLogger("telemetry")

    def log_as_span(self, message, level=logging.INFO):
        with self.tracer.start_as_current_span("logging") as span:
            if level == logging.DEBUG:
                self.logger.debug(message)
            elif level == logging.INFO:
                self.logger.info(message)
            elif level == logging.WARNING:
                self.logger.warning(message)
            elif level == logging.ERROR:
                self.logger.error(message)
            elif level == logging.CRITICAL:
                self.logger.critical(message)
            span.add_event("log_event", {"message": message, "level": level})

    def make_request(self, url):
        try:
            with self.tracer.start_as_current_span("http_request") as span:
                response = requests.get(url)
                self.logger.info(f"Received response: {response.status_code}")
                span.add_event("Received response", {"status_code": response.status_code, "body": response.text})
                return response
        except Exception as e:
            self.logger.exception(f"Exception during request: {e}")
            raise

def main():
    collector_endpoint = "https://otel.helming.xyz"
    service_name = "test_telemetry"
    telemetry = Telemetry(collector_endpoint, service_name)
    telemetry.log_as_span("This is a test log message", level=logging.INFO)
    try:
        response = telemetry.make_request("https://httpbin.org/get")
        telemetry.log_as_span(f"Request successful with status code: {response.status_code}", level=logging.INFO)
    except Exception as e:
        telemetry.log_as_span(f"Request failed with exception: {e}", level=logging.ERROR)

if __name__ == "__main__":
    main()