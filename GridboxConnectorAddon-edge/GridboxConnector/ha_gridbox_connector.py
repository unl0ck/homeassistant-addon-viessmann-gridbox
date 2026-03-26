from ha_mqtt_discoverable import Settings, DeviceInfo
from sensor_model import SensorModel, key_in_model, load_sensor_by_key, create_ha_sensor
import logging
from logging import Logger

class HAGridboxConnector:
    battery_sensor_dict: dict
    mqtt_settings: Settings.MQTT
    device_info: DeviceInfo
    logger: logging.Logger

    def __init__(
        self,
        mqtt_settings,
        device_name: str = "Viessmann Gridbox", #TODO using dynamic name from config file will load over ha setting
        device_identifiers: str = "viessmann_gridbox",
        device_manufacturer: str = "Viessmann",
        device_model: str = "Vitocharge 2.0",
        logger: Logger = logging.getLogger(__name__),
        model_path: str = "models/models.json",
    ):
        self.battery_sensor_dict = {}
        self.ev_sensor_dict = {}
        self.logger = logger
        self.model_path = model_path
        self.mqtt_settings = mqtt_settings
        self.device_info = DeviceInfo(name=device_name, identifiers=device_identifiers, manufacturer=device_manufacturer, model=device_model)
        self.logger.info(f"Device Info: {self.device_info}")

    def _update_sensor(self, attr_name: str, type_key: str, value, sensor_type: str, last_reset: str):
        if not key_in_model(type_key, path=self.model_path, type=sensor_type):
            return
        if not hasattr(self, attr_name):
            setattr(self, attr_name, create_ha_sensor(type_key, self.device_info, self.mqtt_settings, path=self.model_path, type=sensor_type))
        sensor_model = load_sensor_by_key(type_key, path=self.model_path, type=sensor_type)
        if isinstance(value, str):
            getattr(self, attr_name).set_state(value)
        else:
            getattr(self, attr_name).set_state(round(float(value * sensor_model.factor), 2), last_reset=last_reset)

    def update_sensors(self, measurement: dict, last_reset: str = ""):
        for key, data in measurement.items():
            if key in ("battery", "evChargingStation"):
                for type_key, value in data.items():
                    self._update_sensor(f"{key}_{type_key}", type_key, value, key, last_reset)
            elif key in ("heaters", "heatPumps"):
                if data:
                    for type_key, value in data[0].items():
                        self._update_sensor(f"{key}_{type_key}", type_key, value, key, last_reset)
            else:
                if key_in_model(key, path=self.model_path):
                    if not hasattr(self, key):
                        setattr(self, key, create_ha_sensor(key, self.device_info, self.mqtt_settings, path=self.model_path))
                    sensor_model = load_sensor_by_key(key, path=self.model_path)
                    getattr(self, key).set_state(round(float(data) * sensor_model.factor, 2), last_reset=last_reset)
