import os
import json
import time
from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from gridbox_connector import GridboxConnector


if __name__ == '__main__':
    f = open('/build/cloudSettings.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    print("Start Viessmann Connector")
    #print(f"====Version {data["version"]}====")
    
    options_file = open('/data/options.json')
    options_json = json.load(options_file)
    WAIT = int(options_json["wait_time"])
    USER = os.getenv('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    mqtt_user = os.getenv('MqttUser')
    mqtt_pw = os.getenv('MqttPw')
    mqtt_server = os.getenv('MqttServer')
    mqtt_port = os.getenv('MqttPort')
    data["login"]["username"] = USER
    data["login"]["password"] = PASSWORD
    print(data["login"])
    one_time_print = True

    mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw)

    device_info = DeviceInfo(name="Viessmann Gridbox", identifiers="viessmann_gridbox", manufacturer="Viessmann", model="Vitocharge 2.0")

    production_sensor_info = SensorInfo(name="Production", device_class="power", unique_id="gridbox_production", device=device_info, unit_of_measurement="W")
    production_settings = Settings(mqtt=mqtt_settings, entity=production_sensor_info)

    grid_sensor_info = SensorInfo(name="Grid", device_class="power", unique_id="gridbox_grid", device=device_info, unit_of_measurement="W")
    grid_settings = Settings(mqtt=mqtt_settings, entity=grid_sensor_info)

    photovoltaic_sensor_info = SensorInfo(name="Photovoltaic", device_class="power", unique_id="gridbox_photovoltaic", device=device_info, unit_of_measurement="W")
    photovoltaic_settings = Settings(mqtt=mqtt_settings, entity=photovoltaic_sensor_info)

    # consumption
    consumption_household_sensor_info = SensorInfo(name="Consumption", device_class="power", unique_id="gridbox_consumption_household", device=device_info, unit_of_measurement="W")
    consumption_household_settings = Settings(mqtt=mqtt_settings, entity=consumption_household_sensor_info)

    total_consumption_household_sensor_info = SensorInfo(name="Total Consumption", device_class="power", unique_id="total_consumption_household", device=device_info, unit_of_measurement="W")
    total_consumption_household_settings = Settings(mqtt=mqtt_settings, entity=total_consumption_household_sensor_info)
    
    # Direct Consumption
    direct_consumption_household_sensor_info = SensorInfo(name="DirectConsumptionHousehold", device_class="power", unique_id="gridbox_direct_consumption_household", device=device_info, unit_of_measurement="W")
    direct_consumption_household_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_household_sensor_info)

    direct_consumption_heatpump_sensor_info = SensorInfo(name="DirectConsumptionHeatPump", device_class="power", unique_id="gridbox_direct_consumption_heatpump", device=device_info, unit_of_measurement="W")
    direct_consumption_heatpump_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_heatpump_sensor_info)

    direct_consumption_rate_sensor_info = SensorInfo(name="DirectConsumptionRate", device_class="power_factor", unique_id="gridbox_direct_consumption_rate", device=device_info, unit_of_measurement="%")
    direct_consumption_rate_settings = Settings(mqtt=mqtt_settings, entity=direct_consumption_rate_sensor_info)
    
    # Self Consumption
    self_supply_sensor_info = SensorInfo(name="SelfSupply", device_class="power", unique_id="gridbox_self_supply", device=device_info, unit_of_measurement="W")
    self_supply_settings = Settings(mqtt=mqtt_settings, entity=self_supply_sensor_info)
    
    self_consumption_rate_sensor_info = SensorInfo(name="SelfConsumptionRate", device_class="power_factor", unique_id="gridbox_self_consumption_rate", device=device_info, unit_of_measurement="%")
    self_consumption_rate_settings = Settings(mqtt=mqtt_settings, entity=self_consumption_rate_sensor_info)

    # Battery Section
    battery_sensor_info_sum = SensorInfo(name="Battery Sum Level", device_class="battery", unique_id="gridbox_battery_sum", device=device_info, unit_of_measurement="%")
    battery_settings_sum = Settings(mqtt=mqtt_settings, entity=battery_sensor_info_sum)

    battery_sensor_capacity_sum = SensorInfo(name="Battery Sum Capacity", device_class="energy", unique_id="gridbox_battery_level_sum", device=device_info, unit_of_measurement="Wh")
    battery_settings_capacity_sum = Settings(mqtt=mqtt_settings, entity=battery_sensor_capacity_sum)

    battery_sensor_power_sum = SensorInfo(name="Battery Sum Power", device_class="battery", unique_id="gridbox_battery_power_sum", device=device_info, unit_of_measurement="W")
    battery_settings_power_sum = Settings(mqtt=mqtt_settings, entity=battery_sensor_power_sum)

    # Instantiate the sensor
    production_sensor = Sensor(production_settings)
    grid_sensor = Sensor(grid_settings)
    photovoltaic_sensor = Sensor(photovoltaic_settings)

    # Battery
    battery_sum_level = Sensor(battery_settings_sum)
    battery_sum_capacity = Sensor(battery_settings_capacity_sum)
    battery_sum_power = Sensor(battery_settings_power_sum)

    # Consumption
    consumption_household_sensor = Sensor(consumption_household_settings)
    total_consumption_household_sensor = Sensor(total_consumption_household_settings)
    direct_consumption_household_sensor = Sensor(direct_consumption_household_settings)
    direct_consumtion_heatpump_sensor = Sensor(direct_consumption_heatpump_settings)
    direct_consumtion_rate_sensor = Sensor(direct_consumption_rate_settings)
    
    self_supply_sensor = Sensor(self_supply_settings)
    self_consumtion_rate_sensor = Sensor(self_consumption_rate_settings)

    gridboxConnector = GridboxConnector(data)
    while True:
        measurement = gridboxConnector.retrieve_live_data()
        if one_time_print:
            print(measurement)
            one_time_print = False
        if "production" in measurement:
            production_sensor.set_state(measurement["production"])
        if "grid" in measurement:
            grid_sensor.set_state(measurement["grid"])
        if "photovoltaic" in measurement:
            photovoltaic_sensor.set_state(measurement["photovoltaic"])
        if "consumption" in measurement:
            consumption_household_sensor.set_state(measurement["consumption"])
        if "totalConsumption" in measurement:
            total_consumption_household_sensor.set_state(measurement["totalConsumption"])
        if "directConsumptionHousehold" in measurement:
            direct_consumption_household_sensor.set_state(float(measurement["directConsumptionHousehold"]))
        if "directConsumptionHeatPump" in measurement:
            direct_consumtion_heatpump_sensor.set_state(float(measurement["directConsumptionHeatPump"]))
        if "directConsumptionRate" in measurement:
            direct_consumtion_rate_sensor.set_state(float(measurement["directConsumptionRate"])*10)
            
        if "selfSupply" in measurement:
            self_supply_sensor.set_state(float(measurement["selfSupply"]))
        if "selfConsumptionRate" in measurement:
            self_consumtion_rate_sensor.set_state(float(measurement["selfConsumptionRate"])*10)
            
        if "battery" in measurement:
            battery_sum_level.set_state(float(measurement["battery"]["stateOfCharge"])*100)
            battery_sum_capacity.set_state(float(measurement["battery"]["capacity"]))
            battery_sum_power.set_state(float(measurement["battery"]["power"]))
        # Wait until fetch new values in seconds
        time.sleep(WAIT)
