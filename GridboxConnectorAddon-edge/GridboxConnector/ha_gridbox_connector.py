from ha_mqtt_discoverable import Settings, DeviceInfo
from sensor_model import SensorModel, key_in_model, load_sensor_by_key, create_ha_sensor
import logging
from logging import Logger
import json

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

    def update_sensors(self, measurement: dict, last_reset: str = ""):
        for key in measurement.keys():
            if key == "battery" or key == "evChargingStation":
                type = key
                type_json = measurement.get(key, {})
                for type_key in type_json.keys():
                    attr_name = f"{type}_{type_key}"
                    if key_in_model(type_key, path=self.model_path, type=type):
                        if not hasattr(self, attr_name):
                            setattr(self, attr_name, create_ha_sensor(type_key, self.device_info, self.mqtt_settings, path=self.model_path, type=type))
                        sensor_model = load_sensor_by_key(type_key, path=self.model_path, type=type)
                        getattr(self, attr_name).set_state(round(float(type_json.get(type_key, "0") * sensor_model.factor), 2), last_reset=last_reset)
            elif key == "heaters":
                type = "heaters"
                heaters = measurement.get("heaters", [])
                heater = heaters[0]
                for type_key in heater.keys():
                    attr_name = f"{type}_{type_key}"
                    if key_in_model(type_key, path=self.model_path, type=type):
                        if not hasattr(self, attr_name):
                            setattr(self, attr_name, create_ha_sensor(type_key, self.device_info, self.mqtt_settings, path=self.model_path, type=type))
                        sensor_model = load_sensor_by_key(type_key, path=self.model_path, type=type)
                        getattr(self, attr_name).set_state(round(float(heater.get(type_key, "0") * sensor_model.factor), 2), last_reset=last_reset)
            else:
                if key_in_model(key, path=self.model_path):
                    if not hasattr(self, key):
                        setattr(self, key, create_ha_sensor(key, self.device_info, self.mqtt_settings, path=self.model_path))
                    sensor_model = load_sensor_by_key(key, path=self.model_path)
                    getattr(self, key).set_state(round(float(measurement.get(key, "0")) * sensor_model.factor, 2), last_reset=last_reset)