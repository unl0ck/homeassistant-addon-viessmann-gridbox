import os
import json
import time
from gridbox_connector import GridboxConnector
from ha_mqtt_discoverable import Settings
from ha_viessmann_gridbox_connector import HAViessmannGridboxConnector

if __name__ == '__main__':
    f = open('/build/cloudSettings.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    f.close()
    print("Start Viessmann Connector")
    # print(f"====Version {data["version"]}====")

    options_file = open('/data/options.json')
    options_json = json.load(options_file)
    WAIT = int(options_json["wait_time"])
    USER = os.getenv('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    mqtt_user = os.getenv('MqttUser', "")
    mqtt_pw = os.getenv('MqttPw', "")
    mqtt_server = os.getenv('MqttServer', "")
    mqtt_port = os.getenv('MqttPort', "")
    data["login"]["username"] = USER
    data["login"]["password"] = PASSWORD
    print(data["login"])
    one_time_print = True
    mqtt_settings = Settings.MQTT(
        host=mqtt_server, username=mqtt_user, password=mqtt_pw)
    viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)
    gridboxConnector = GridboxConnector(data)
    while True:
        measurement = gridboxConnector.retrieve_live_data()
        viessmann_gridbox_connector.update_sensors(measurement)
        if one_time_print:
            print(measurement)
            one_time_print = False
        # Wait until fetch new values in seconds
        time.sleep(WAIT)
