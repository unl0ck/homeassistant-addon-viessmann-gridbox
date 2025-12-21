from ha_mqtt_discoverable import Settings, DeviceInfo
from sensor_model import SensorModel, key_in_model, load_sensor_by_key, create_ha_sensor
import logging
from logging import Logger
import json


class HAViessmannGridboxConnector:
    battery_sensor_dict: dict
    mqtt_settings: Settings.MQTT
    device_info: DeviceInfo
    logger: logging.Logger

    def __init__(
        self,
        mqtt_settings,
        device_name: str = "Viessmann Gridbox",
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

        # with open(self.model_path) as f:
        #     sensors: dict = json.load(f)
        #     for key in sensors.keys():
        #         try:
        #             self[key] = create_ha_sensor(key)
        #         except ValueError as e:
        #             self.logger.error(e)
        #             continue
        # # Instantiate the sensors
        # self.production_sensor = create_ha_sensor("production", self.device_info, mqtt_settings, path=self.model_path)
        # self.grid_sensor = create_ha_sensor("grid", self.device_info, mqtt_settings, path=self.model_path)
        # self.photovoltaic_sensor = create_ha_sensor("photovoltaic", self.device_info, mqtt_settings, path=self.model_path)
        # self.consumption_household_sensor = create_ha_sensor("consumption", self.device_info, mqtt_settings, path=self.model_path)
        # self.total_consumption_household_sensor = create_ha_sensor("totalConsumption", self.device_info, mqtt_settings, path=self.model_path)
        # self.direct_consumption_household_sensor = create_ha_sensor("directConsumptionHousehold", self.device_info, mqtt_settings, path=self.model_path)
        # self.direct_consumption_heatpump_sensor = create_ha_sensor("directConsumptionHeatPump", self.device_info, mqtt_settings, path=self.model_path)
        # self.direct_consumption_ev_sensor = create_ha_sensor("directConsumptionEV", self.device_info, mqtt_settings, path=self.model_path)
        # self.direct_consumption_rate_sensor = create_ha_sensor("directConsumptionRate", self.device_info, mqtt_settings, path=self.model_path)
        # self.self_supply_sensor = create_ha_sensor("selfSupply", self.device_info, mqtt_settings, path=self.model_path)
        # self.self_consumtion_rate_sensor = create_ha_sensor("selfConsumptionRate", self.device_info, mqtt_settings, path=self.model_path)
        # self.self_sufficiency_rate_sensor = create_ha_sensor("selfSufficiencyRate", self.device_info, mqtt_settings, path=self.model_path)

        # # Battery sum
        # self.battery_sum = HAViessmannBattery(mqtt_settings, self.device_info, "sum", "")

        # # Heater
        # self.heater_sensor = HAViessmannHeater(mqtt_settings, self.device_info, "", "")

        # # EV
        # self.ev_sum = HAViessmannEVChargingStation(mqtt_settings, self.device_info, "sum", "")

    def update_sensors(self, measurement: dict, last_reset: str = None):
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