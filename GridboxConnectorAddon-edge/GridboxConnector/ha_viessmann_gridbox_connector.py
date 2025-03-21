from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from ha_viessmann_battery import HAViessmannBattery
from ha_viessmann_ev_charging_station import HAViessmannEVChargingStation
from ha_viessmann_heater import HAViessmannHeater
from sensor_model import SensorModel, key_in_model, load_sensor_by_key, create_ha_sensor
import logging
from logging import Logger
import json


class HAViessmannGridboxConnector:
    battery_sensor_dict: dict
    mqtt_settings: Settings.MQTT
    device_info: DeviceInfo
    production_sensor: Sensor
    grid_sensor: Sensor
    photovoltaic_sensor: Sensor
    consumption_household_sensor: Sensor
    total_consumption_household_sensor: Sensor
    direct_consumption_household_sensor: Sensor
    direct_consumption_heatpump_sensor: Sensor
    direct_consumption_ev_sensor: Sensor
    direct_consumption_heater_sensor: Sensor
    direct_consumption_rate_sensor: Sensor
    self_supply_sensor: Sensor
    self_consumtion_rate_sensor: Sensor
    self_sufficiency_rate_sensor: Sensor
    battery_sum: HAViessmannBattery
    heater_sensor: HAViessmannHeater
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
                type_json = measurement.get("battery", {})
                for type_key in type_json.keys():
                    if key_in_model(type_key, path=self.model_path, type=type):
                        if f"{type}_{type_key}" not in self:
                            self[f"{type}_{type_key}"] = create_ha_sensor(type_key, self.device_info, self.mqtt_settings, path=self.model_path, type=type)
                        sensor_model = load_sensor_by_key(type_key, path=self.model_path, type=type)
                        self[f"{type}_{type_key}"].set_state(round(float(type_json.get(type_key, "0") * sensor_model.factor), 2), last_reset=last_reset)
            elif key == "heaters":
                type = "heaters"
                heaters = measurement.get("heaters", [])
                heater = heaters[0]
                for type_key in heater.keys():
                    if key_in_model(type_key, path=self.model_path, type=type):
                        if f"{type}_{type_key}" not in self:
                            self[f"{type}_{type_key}"] = create_ha_sensor(type_key, self.device_info, self.mqtt_settings, path=self.model_path, type=type)
                        sensor_model = load_sensor_by_key(type_key, path=self.model_path, type=type)
                        self[f"{type}_{type_key}"].set_state(round(float(type_json.get(type_key, "0") * sensor_model.factor), 2), last_reset=last_reset)
            else:
                if key_in_model(key, path=self.model_path):
                    if key not in self:
                        self[key] = create_ha_sensor(key, self.device_info, self.mqtt_settings, path=self.model_path)
                    sensor_model = load_sensor_by_key(type_key, path=self.model_path)
                    self[key].set_state(round(float(measurement.get(key, "0") * sensor_model.factor), 2), last_reset=last_reset)
        # if "production" in measurement:
        #     self.production_sensor.set_state(measurement.get("production", ""), last_reset=last_reset)
        # else:
        #     self.logger.warning("No production data received")
        # if "grid" in measurement:
        #     self.grid_sensor.set_state(measurement.get("grid", ""), last_reset=last_reset)
        # else:
        #     self.logger.warning("No grid data received")
        # if "photovoltaic" in measurement:
        #     self.photovoltaic_sensor.set_state(measurement.get("photovoltaic", ""), last_reset=last_reset)
        # else:
        #     self.logger.warning("No photovoltaic data received")
        # if "consumption" in measurement:
        #     self.consumption_household_sensor.set_state(measurement.get("consumption", ""), last_reset=last_reset)
        # else:
        #     self.logger.warning("No consumption data received")
        # if "totalConsumption" in measurement:
        #     self.total_consumption_household_sensor.set_state(measurement.get("totalConsumption", ""), last_reset=last_reset)
        # else:
        #     self.logger.warning("No total consumption data received")
        # if "directConsumptionHousehold" in measurement:
        #     self.direct_consumption_household_sensor.set_state(float(measurement.get("directConsumptionHousehold", "0")), last_reset=last_reset)
        # if "directConsumptionHeatPump" in measurement:
        #     self.direct_consumption_heatpump_sensor.set_state(float(measurement.get("directConsumptionHeatPump", "0")), last_reset=last_reset)
        # if "directConsumptionEV" in measurement:
        #     self.direct_consumption_ev_sensor.set_state(float(measurement.get("directConsumptionEV", "0")), last_reset=last_reset)
        # if "directConsumptionRate" in measurement:
        #     self.direct_consumption_rate_sensor.set_state(round(float(measurement.get("directConsumptionRate", "0")) * 100, 2))

        # if "selfSupply" in measurement:
        #     self.self_supply_sensor.set_state(float(measurement.get("selfSupply", "")), last_reset=last_reset)
        # if "selfConsumptionRate" in measurement:
        #     self.self_consumtion_rate_sensor.set_state(round(float(measurement.get("selfConsumptionRate", "0")) * 100, 2))
        # if "selfSufficiencyRate" in measurement:
        #     self.self_sufficiency_rate_sensor.set_state(round(float(measurement.get("selfSufficiencyRate", "0")) * 100, 2))

        # if "battery" in measurement:
        #     battery: dict = measurement.get("battery", {})
        #     state_of_charge = float(battery.get("stateOfCharge", "0")) * 100
        #     capacity = float(battery.get("capacity", "0"))
        #     power = float(battery.get("power", "0"))
        #     remaining_charge = float(battery.get("remainingCharge", "0"))
        #     self.battery_sum.set_states(state_of_charge, capacity, power, remaining_charge)

        # if "batteries" in measurement:
        #     batteries: list = measurement.get("batteries", [])
        #     for index, battery in enumerate(batteries):
        #         appliance_id = battery.get("applianceID", "")
        #         if appliance_id not in self.battery_sensor_dict:
        #             self.battery_sensor_dict[appliance_id] = HAViessmannBattery(self.mqtt_settings, self.device_info, f"{index + 1}", appliance_id)
        #         battery_sensor = self.battery_sensor_dict[appliance_id]
        #         state_of_charge = float(battery.get("stateOfCharge", "0")) * 100
        #         capacity = float(battery.get("capacity", "0"))
        #         power = float(battery.get("power", "0"))
        #         remaining_charge = float(battery.get("remainingCharge", "0"))
        #         battery_sensor.set_states(state_of_charge, capacity, power, remaining_charge)

        # if "heaters" in measurement:
        #     heaters: list = measurement.get("heaters", [])
        #     heater = heaters[0]
        #     appliance_id = heater.get("applianceID", "")
        #     power = round(float(heater.get("power", "0")), 0)
        #     temperature = round(float(heater.get("temperature", "0")), 1)
        #     self.heater_sensor.set_states(power, temperature)

        # if "evChargingStation" in measurement:
        #     ev_charging_station: dict = measurement.get("evChargingStation", {})
        #     power = float(ev_charging_station.get("power", "0"))
        #     state_of_charge = float(ev_charging_station.get("stateOfCharge", "0")) * 100
        #     current_l1 = float(ev_charging_station.get("currentL1", "0"))
        #     current_l2 = float(ev_charging_station.get("currentL2", "0"))
        #     current_l3 = float(ev_charging_station.get("currentL3", "0"))
        #     reading_total = float(ev_charging_station.get("readingTotal", "0"))
        #     self.ev_sum.set_states(power, state_of_charge, current_l1, current_l2, current_l3, reading_total)

        # if "evChargingStations" in measurement:
        #     ev_charging_stations: list = measurement.get("evChargingStations", [])
        #     for index, ev_charging_station in enumerate(ev_charging_stations):
        #         appliance_id = ev_charging_station.get("applianceID", "")
        #         if appliance_id not in self.ev_sensor_dict:
        #             self.ev_sensor_dict[appliance_id] = HAViessmannEVChargingStation(self.mqtt_settings, self.device_info, f"{index + 1}", appliance_id)
        #         ev_charging_station_sensor = self.ev_sensor_dict[appliance_id]
        #         power = float(ev_charging_station.get("power", "0"))
        #         state_of_charge = float(ev_charging_station.get("stateOfCharge", "0")) * 100
        #         current_l1 = float(ev_charging_station.get("currentL1", "0"))
        #         current_l2 = float(ev_charging_station.get("currentL2", "0"))
        #         current_l3 = float(ev_charging_station.get("currentL3", "0"))
        #         reading_total = float(ev_charging_station.get("readingTotal", "0"))
        #         ev_charging_station_sensor.set_states(power, state_of_charge, current_l1, current_l2, current_l3, reading_total)
