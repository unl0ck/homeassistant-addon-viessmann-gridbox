from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from ha_viessmann_battery import HAViessmannBattery
from ha_viessmann_ev_charging_station import HAViessmannEVChargingStation
from ha_viessmann_heater import HAViessmannHeater
import logging


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

    def __init__(self, mqtt_settings, device_name="Viessmann Gridbox", device_identifiers="viessmann_gridbox", device_manufacturer="Viessmann", device_model="Vitocharge 2.0", prefix="", logger=logging.getLogger(__name__),device_class_of_power="power", unit_of_power="W",state_class=None):
        self.battery_sensor_dict = {}
        self.ev_sensor_dict = {}
        self.logger = logger
        self.mqtt_settings = mqtt_settings
        self.device_info = DeviceInfo(
            name=device_name, identifiers=device_identifiers, manufacturer=device_manufacturer, model=device_model)
        self.logger.info(f"Device Info: {self.device_info}")
        production_sensor_info = SensorInfo(name="Production", device_class=device_class_of_power, unique_id="gridbox_production"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        production_settings = Settings(mqtt=mqtt_settings, entity=production_sensor_info)

        grid_sensor_info = SensorInfo(name="Grid", device_class=device_class_of_power, unique_id="gridbox_grid"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        grid_settings = Settings(mqtt=mqtt_settings, entity=grid_sensor_info)

        photovoltaic_sensor_info = SensorInfo(name="Photovoltaic", device_class=device_class_of_power, unique_id="gridbox_photovoltaic"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        photovoltaic_settings = Settings(mqtt=mqtt_settings, entity=photovoltaic_sensor_info)

        # consumption
        consumption_household_sensor_info = SensorInfo(name="Consumption", device_class=device_class_of_power, unique_id="gridbox_consumption_household"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        consumption_household_settings = Settings(mqtt=mqtt_settings, entity=consumption_household_sensor_info)

        total_consumption_household_sensor_info = SensorInfo(name="Total Consumption", device_class=device_class_of_power, unique_id="total_consumption_household"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        total_consumption_household_settings = Settings(mqtt=mqtt_settings, entity=total_consumption_household_sensor_info)

        # Direct Consumption
        direct_consumption_household_sensor_info = SensorInfo(name="DirectConsumptionHousehold", device_class=device_class_of_power, unique_id="gridbox_direct_consumption_household"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        direct_consumption_household_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_household_sensor_info)

        direct_consumption_heatpump_sensor_info = SensorInfo(name="DirectConsumptionHeatPump", device_class=device_class_of_power, unique_id="gridbox_direct_consumption_heatpump"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        direct_consumption_heatpump_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_heatpump_sensor_info)

        direct_consumption_ev_sensor_info = SensorInfo(name="DirectConsumptionEV", device_class=device_class_of_power, unique_id="gridbox_direct_consumption_ev"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        direct_consumption_ev_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_ev_sensor_info)

        direct_consumption_rate_sensor_info = SensorInfo(name="DirectConsumptionRate", device_class="power_factor", unique_id="gridbox_direct_consumption_rate"+prefix, device=self.device_info, unit_of_measurement="%")
        direct_consumption_rate_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_rate_sensor_info)

        # Self Consumption
        self_supply_sensor_info = SensorInfo(name="SelfSupply", device_class=device_class_of_power,unique_id="gridbox_self_supply"+prefix, device=self.device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        self_supply_settings = Settings(mqtt=mqtt_settings, entity=self_supply_sensor_info)

        self_consumption_rate_sensor_info = SensorInfo(name="SelfConsumptionRate", device_class="power_factor", unique_id="gridbox_self_consumption_rate"+prefix, device=self.device_info, unit_of_measurement="%")
        self_consumption_rate_settings = Settings(mqtt=mqtt_settings, entity=self_consumption_rate_sensor_info)

        self_sufficiency_rate_sensor_info = SensorInfo(name="SelfSufficiencyRate", device_class="power_factor", unique_id="gridbox_self_sufficiency_rate"+prefix, device=self.device_info, unit_of_measurement="%")
        self_sufficiency_rate_settings = Settings(mqtt=mqtt_settings, entity=self_sufficiency_rate_sensor_info)

        # Instantiate the sensors

        self.production_sensor = Sensor(production_settings)
        self.grid_sensor = Sensor(grid_settings)
        self.photovoltaic_sensor = Sensor(photovoltaic_settings)

        # Battery sum
        self.battery_sum = HAViessmannBattery(mqtt_settings, self.device_info, "sum", "", prefix, unit_of_power, state_class)

        # Heater
        self.heater_sensor = HAViessmannHeater(mqtt_settings, self.device_info, "", "", prefix)

        # EV
        self.ev_sum = HAViessmannEVChargingStation(mqtt_settings, self.device_info, "sum", "", prefix)

        # Consumption
        self.consumption_household_sensor = Sensor(consumption_household_settings)
        self.total_consumption_household_sensor = Sensor(total_consumption_household_settings)
        self.direct_consumption_household_sensor = Sensor(direct_consumption_household_settings)
        self.direct_consumption_heatpump_sensor = Sensor(direct_consumption_heatpump_settings)
        self.direct_consumption_ev_sensor = Sensor(direct_consumption_ev_settings)
        self.direct_consumption_rate_sensor = Sensor(direct_consumption_rate_settings)

        self.self_supply_sensor = Sensor(self_supply_settings)
        self.self_consumtion_rate_sensor = Sensor(self_consumption_rate_settings)
        self.self_sufficiency_rate_sensor = Sensor(self_sufficiency_rate_settings)

    def update_sensors(self, measurement: dict, last_reset: str = None):
        if "production" in measurement:
            self.production_sensor.set_state(measurement.get("production", ""), last_reset=last_reset)
        else:
            self.logger.warning("No production data received")
        if "grid" in measurement:
            self.grid_sensor.set_state(measurement.get("grid", ""), last_reset=last_reset)
        else:
            self.logger.warning("No grid data received")
        if "photovoltaic" in measurement:
            self.photovoltaic_sensor.set_state(measurement.get("photovoltaic", ""), last_reset=last_reset)
        else:
            self.logger.warning("No photovoltaic data received")
        if "consumption" in measurement:
            self.consumption_household_sensor.set_state(measurement.get("consumption", ""), last_reset=last_reset)
        else:
            self.logger.warning("No consumption data received")
        if "totalConsumption" in measurement:
            self.total_consumption_household_sensor.set_state(measurement.get("totalConsumption", ""), last_reset=last_reset)
        else:
            self.logger.warning("No total consumption data received")
        if "directConsumptionHousehold" in measurement:
            self.direct_consumption_household_sensor.set_state(float(measurement.get("directConsumptionHousehold", "0")), last_reset=last_reset)
        if "directConsumptionHeatPump" in measurement:
            self.direct_consumption_heatpump_sensor.set_state(float(measurement.get("directConsumptionHeatPump", "0")), last_reset=last_reset)
        if "directConsumptionEV" in measurement:
            self.direct_consumption_ev_sensor.set_state(float(measurement.get("directConsumptionEV", "0")), last_reset=last_reset)
        if "directConsumptionRate" in measurement:
            self.direct_consumption_rate_sensor.set_state(round(float(measurement.get("directConsumptionRate", "0"))*100,2))

        if "selfSupply" in measurement:
            self.self_supply_sensor.set_state(float(measurement.get("selfSupply", "")), last_reset=last_reset)
        if "selfConsumptionRate" in measurement:
            self.self_consumtion_rate_sensor.set_state(round(float(measurement.get("selfConsumptionRate", "0"))*100,2))
        if "selfSufficiencyRate" in measurement:
            self.self_sufficiency_rate_sensor.set_state(round(float(measurement.get("selfSufficiencyRate", "0"))*100,2))

        if "battery" in measurement:
            battery: dict = measurement.get("battery", {})
            state_of_charge = float(battery.get("stateOfCharge", "0"))*100
            capacity = float(battery.get("capacity", "0"))
            power = round(float(battery.get("power", "0")),2)
            remaining_charge = round(float(battery.get("remainingCharge", "0")),2)
            charge = round(float(battery.get("charge", "-1")),2)
            discharge = round(float(battery.get("discharge", "-1")),2)
            self.battery_sum.set_states(state_of_charge, capacity, power, remaining_charge, charge, discharge, last_reset)

        if "batteries" in measurement:
            batteries: list = measurement.get("batteries", [])
            for index, battery in enumerate(batteries):
                appliance_id = battery.get("applianceID", "")
                if appliance_id not in self.battery_sensor_dict:
                    self.battery_sensor_dict[appliance_id] = HAViessmannBattery(self.mqtt_settings, self.device_info, f"{index+1}", appliance_id)
                battery_sensor = self.battery_sensor_dict[appliance_id]
                state_of_charge = float(battery.get("stateOfCharge", "0"))*100
                capacity = float(battery.get("capacity", "0"))
                power = float(battery.get("power", "0"))
                remaining_charge = float(battery.get("remainingCharge", "0"))
                battery_sensor.set_states(state_of_charge, capacity, power, remaining_charge)

        if "heaters" in measurement:
            heaters: list = measurement.get("heaters", [])
            heater = heaters[0]
            appliance_id = heater.get("applianceID", "")
            power = round(float(heater.get("power", "0")),0)
            temperature = round(float(heater.get("temperature", "0")),1)
            self.heater_sensor.set_states(power, temperature)

        if "evChargingStation" in measurement:
            ev_charging_station: dict = measurement.get("evChargingStation", {})
            power = float(ev_charging_station.get("power", "0"))
            state_of_charge = float(ev_charging_station.get("stateOfCharge", "0"))*100
            current_l1 = float(ev_charging_station.get("currentL1", "0"))
            current_l2 = float(ev_charging_station.get("currentL2", "0"))
            current_l3 = float(ev_charging_station.get("currentL3", "0"))
            reading_total = float(ev_charging_station.get("readingTotal", "0"))
            self.ev_sum.set_states(power, state_of_charge, current_l1, current_l2, current_l3, reading_total)

        if "evChargingStations" in measurement:
            ev_charging_stations: list = measurement.get("evChargingStations", [])
            for index, ev_charging_station in enumerate(ev_charging_stations):
                appliance_id = ev_charging_station.get("applianceID", "")
                if appliance_id not in self.ev_sensor_dict:
                    self.ev_sensor_dict[appliance_id] = HAViessmannEVChargingStation(self.mqtt_settings, self.device_info, f"{index+1}", appliance_id)
                ev_charging_station_sensor = self.ev_sensor_dict[appliance_id]
                power = float(ev_charging_station.get("power", "0"))
                state_of_charge = float(ev_charging_station.get("stateOfCharge", "0"))*100
                current_l1 = float(ev_charging_station.get("currentL1", "0"))
                current_l2 = float(ev_charging_station.get("currentL2", "0"))
                current_l3 = float(ev_charging_station.get("currentL3", "0"))
                reading_total = float(ev_charging_station.get("readingTotal", "0"))
                ev_charging_station_sensor.set_states(power, state_of_charge, current_l1, current_l2, current_l3, reading_total)
