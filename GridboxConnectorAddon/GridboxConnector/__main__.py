import os
import json
from GridboxConnector import GridboxConnector
import time
from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo

if __name__ == '__main__':
    f = open('/build/cloudSettings.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    print("Start Viessmann Connector")
    #print("====Version {}====".format(data["version"])
    
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
    # Configure the required parameters for the MQTT broker
    mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw)

    # Define the device. At least one of `identifiers` or `connections` must be supplied
    device_info = DeviceInfo(name="Viessmann Gridbox", identifiers="viessmann_gridbox", manufacturer="Viessmann", model="Vitocharge 2.0")

    # Associate the sensor with the device via the `device` parameter
    # `unique_id` must also be set, otherwise Home Assistant will not display the device in the UI
    production_sensor_info = SensorInfo(name="Production", device_class="power", unique_id="gridbox_production", device=device_info, unit_of_measurement="W")
    production_settings = Settings(mqtt=mqtt_settings, entity=production_sensor_info)

    grid_sensor_info = SensorInfo(name="Grid", device_class="power", unique_id="gridbox_grid", device=device_info, unit_of_measurement="W")
    grid_settings = Settings(mqtt=mqtt_settings, entity=grid_sensor_info)

    photovoltaic_sensor_info = SensorInfo(name="Photovoltaic", device_class="power", unique_id="gridbox_photovoltaic", device=device_info, unit_of_measurement="W")
    photovoltaic_settings = Settings(mqtt=mqtt_settings, entity=photovoltaic_sensor_info)

    #Battery Section
    
    battery_sensor_info_sum = SensorInfo(name="Battery Sum Level", device_class="battery", unique_id="gridbox_battery_sum", device=device_info, unit_of_measurement="%")
    battery_settings_sum = Settings(mqtt=mqtt_settings, entity=battery_sensor_info_sum)

    battery_sensor_capacity_sum = SensorInfo(name="Battery Sum Capacity", device_class="battery", unique_id="gridbox_battery_level_sum", device=device_info, unit_of_measurement="Wh")
    battery_settings_capacity_sum = Settings(mqtt=mqtt_settings, entity=battery_sensor_capacity_sum)

    battery_sensor_power_sum = SensorInfo(name="Battery Sum Power", device_class="battery", unique_id="gridbox_battery_power_sum", device=device_info, unit_of_measurement="W")
    battery_settings_power_sum = Settings(mqtt=mqtt_settings, entity=battery_sensor_power_sum)

    # Instantiate the sensor
    production_sensor = Sensor(production_settings)
    grid_sensor = Sensor(grid_settings)
    photovoltaic_sensor = Sensor(photovoltaic_settings)

    #Battery Section
    battery_sum_level = Sensor(battery_settings_sum)
    battery_sum_capacity = Sensor(battery_settings_capacity_sum)
    battery_sum_power = Sensor(battery_settings_power_sum)

    gridboxConnector = GridboxConnector(data)
    while True:
        measurement = gridboxConnector.retrieve_live_data()
        if one_time_print:
            print(measurement)
            one_time_print = False
        if "production" in measurement:
            production_sensor.set_state(measurement["production"])
            grid_sensor.set_state(measurement["grid"])
            photovoltaic_sensor.set_state(measurement["photovoltaic"])
            if "battery" in measurement:
                battery_sum_level.set_state(float(measurement["battery"]["stateOfCharge"])*100)
                battery_sum_capacity.set_state(float(measurement["battery"]["capacity"]))
                battery_sum_power.set_state(float(measurement["battery"]["power"]))
        else:
            print("measurement does not have values {}".format(measurement))
            gridboxConnector = GridboxConnector(data)
        
       
        time.sleep(WAIT)
