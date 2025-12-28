import os
import json
import time
from gridx_connector import GridboxConnector
from ha_mqtt_discoverable import Settings
from ha_gridbox_connector import HAGridboxConnector
import logging
from importlib.resources import files
from utils import SensitiveDataFilter, get_bool_env
import threading
import logfire
import configparser
import sys

opens_file_path = "/data/options.json"
setup_file_path = "setup.ini"
historical_model_path = "./models/models_historical.json"
live_model_path = "./models/models.json"
# Erstellen Sie eine ConfigParser-Instanz
config = configparser.ConfigParser()
# Lesen Sie die setup.ini-Datei
config.read(setup_file_path)
# logging.basicConfig(format='%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addFilter(SensitiveDataFilter())

try:
    logfire_token = os.getenv("LOGFIRE_TOKEN_EDGE", "")
    if os.getenv("OVERRIDE_LOGFIRE_TOKEN", "") != "":
        logfire_token = os.getenv("OVERRIDE_LOGFIRE_TOKEN", logfire_token)
    enable_telemetry = os.getenv("ENABLE_TELEMETRY", "false")
    if enable_telemetry == "false":
        enable_telemetry = False
    elif enable_telemetry == "true":
        enable_telemetry = True

    if not enable_telemetry:
        logger.warning(f"No log fire token")
    else:
        logger.warning(f"Log fire token found {logfire_token}")

    if logfire_token and enable_telemetry:
        logger.info(f"===============================================================")
        logger.info(f"Telemetry to Logfire is {'enabled' if enable_telemetry else 'disabled'}")
        logger.info(f"Will only logs ERROR to Logfire")
        logger.info(f"===============================================================")

        environment = config.get("logfire", "environment", fallback="edge")
        logfire.configure(environment=environment, token=logfire_token)
        logfire.instrument_requests()
        logfire_handler = logfire.LogfireLoggingHandler()
        logfire_handler.setLevel(logging.getLevelName(os.getenv("LOG_LEVEL_TELEMETRY", "ERROR")))
        logger.addHandler(logfire_handler)
except Exception as e:
    logger.error(f"Error configuring logfire: {e}")


def load_gridbox_config():
    config_file = files("gridx_connector").joinpath("eon-home.config.json")
    with open(str(config_file)) as json_file:
        data = json.load(json_file)
    return data


def live_data_task(gridboxConnector: GridboxConnector, ha_viessmann_device: HAGridboxConnector, WAIT):
    one_time_print = True
    while True:
        measurement = gridboxConnector.retrieve_live_data()
        if len(measurement) > 0:
            result = measurement[0]
            ha_viessmann_device.update_sensors(result)
            if one_time_print or logger.level == logging.DEBUG:
                logger.info(result)
                one_time_print = False
            # Wait until fetch new values in seconds
        else:
            logger.warning("No data received")
            gridboxConnector.init_auth()
        time.sleep(WAIT)


def historical_data_task(gridboxConnector: GridboxConnector, ha_viessmann_historical_device: HAGridboxConnector, WAIT):
    one_time_print = True

    while True:
        import time
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone(timedelta(hours=1)))
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today = now.isoformat()
        tomorrow = (now + timedelta(days=1)).isoformat()
        measurement = gridboxConnector.retrieve_historical_data(today, tomorrow)
        midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if len(measurement) > 0:
            result = measurement[0]
            total = result["total"]
            ha_viessmann_historical_device.update_sensors(total, last_reset=midnight_today.isoformat())
            if one_time_print or logger.level == logging.DEBUG:
                logger.info(total)
                one_time_print = False
        else:
            logger.warning("No data received I will Refresh token")
            gridboxConnector.init_auth()
        time.sleep(WAIT)


def start_thread(target, args):
    while True:
        try:
            if sys.is_finalizing():
                logger.info("Interpreter is finalizing, not starting new thread")
                return
            thread = threading.Thread(target=target, args=args)
            thread.start()
            thread.join()
        except Exception as e:
            logger.error(f"Thread konnte nicht gestartet werden: {e}")
            time.sleep(5)  # Warte 5 Sekunden bevor der Thread neu gestartet wird


def start_live_thread(gridboxConnector, ha_device, WAIT):
    logger.info("Start live thread")
    start_thread(live_data_task, (gridboxConnector, ha_device, WAIT))


def start_historical_thread(gridboxConnector: GridboxConnector, ha_device, WAIT):
    logger.info("Start historical thread")
    start_thread(historical_data_task, (gridboxConnector, ha_device, WAIT))


def run_addon():
    gridbox_config = load_gridbox_config()
    options_file = ""
    WAIT = int(os.getenv("WAITTIME", "60"))
    if WAIT < 60:
        WAIT = 60
    if os.path.exists(opens_file_path):
        options_file = open(opens_file_path)
        options_json = json.load(options_file)
        WAIT = int(options_json["wait_time"])

    def find_file(start_path, target_file):
        try:
            for root, dirs, files in os.walk(start_path):
                if target_file in files:
                    return os.path.join(root, target_file)
            return ""
        except Exception as e:
            logger.error(f"Error searching for file {target_file} under {start_path}: {e}")
            return ""

    # Example usage
    start_path = "./"
    target_file = "models_historical.json"  # Replace with the file you are searching for
    found_path = find_file(start_path, target_file)
    historical_model_path = found_path
    target_file = "models.json"  # Replace with the file you are searching for
    found_path = find_file(start_path, target_file)
    live_model_path = found_path
    if found_path:
        logger.info(f"File found: {found_path}")
    else:
        logger.warning(f"File {target_file} not found in {start_path}")

    if not os.path.exists(historical_model_path):
        logger.error("Historical model file not found")
        exit(1)
    if not os.path.exists(live_model_path):
        logger.error("Live model file not found")
        exit(1)

    USER = os.getenv("USERNAME", "")
    PASSWORD = os.environ.get("PASSWORD", "")
    mqtt_user = os.getenv("MqttUser", "")
    mqtt_pw = os.getenv("MqttPw", "")
    mqtt_server = os.getenv("MqttServer", "")
    mqtt_port = os.getenv("MqttPort", "")

    if not USER or not PASSWORD:
        logger.error("Username or Password not set")
        exit(1)
    if not mqtt_user or not mqtt_pw or not mqtt_server or not mqtt_port:
        logger.error("MQTT settings not set")
        exit(1)
    gridbox_config["login"]["username"] = USER
    gridbox_config["login"]["password"] = PASSWORD

    logger.debug(gridbox_config["login"])

    mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw, port=int(mqtt_port))

    viessmann_gridbox_device = HAGridboxConnector(mqtt_settings=mqtt_settings, logger=logger, model_path=live_model_path)
    viessmann_gridbox_historical_device = HAGridboxConnector(
        mqtt_settings=mqtt_settings, device_name="Viessmann Gridbox Historical", device_identifiers="viessmann_gridbox_historical", logger=logger, model_path=historical_model_path
    )

    gridboxConnector = GridboxConnector(gridbox_config)

    # Starte die Threads
    threading.Thread(target=start_live_thread, args=(gridboxConnector, viessmann_gridbox_device, WAIT)).start()
    threading.Thread(target=start_historical_thread, args=(gridboxConnector, viessmann_gridbox_historical_device, WAIT)).start()


if __name__ == "__main__":
    run_addon()
    # run_test_log()
