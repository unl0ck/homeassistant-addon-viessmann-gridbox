import os
import json
import time
from viessmann_gridbox_connector import GridboxConnector
from ha_mqtt_discoverable import Settings
from ha_viessmann_gridbox_connector import HAViessmannGridboxConnector
import logging
from importlib.resources import files
from utils import SensitiveDataFilter
opens_file_path = '/data/options.json'
#logging.basicConfig(format='%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO')))
formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
# Benutzerdefinierten Filter zum Logger hinzufügen
logger.addFilter(SensitiveDataFilter())

def load_gridbox_config():
    config_file = files('viessmann_gridbox_connector').joinpath('config.json')
    with open(str(config_file)) as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    gridbox_config = load_gridbox_config()
    options_file = ''
    WAIT = int(os.getenv('WAITTIME', "60"))
    if os.path.exists(opens_file_path):
        options_file = open(opens_file_path)
        options_json = json.load(options_file)
        WAIT = int(options_json["wait_time"])


    USER = os.getenv('USERNAME', "")
    PASSWORD = os.environ.get('PASSWORD', "")
    mqtt_user = os.getenv('MqttUser', "")
    mqtt_pw = os.getenv('MqttPw', "")
    mqtt_server = os.getenv('MqttServer', "")
    mqtt_port = os.getenv('MqttPort', "")
    if not USER or not PASSWORD:
        logger.error("Username or Password not set")
        exit(1)
    if not mqtt_user or not mqtt_pw or not mqtt_server or not mqtt_port:
        logger.error("MQTT settings not set")
        exit(1)
    gridbox_config["login"]["username"] = USER
    gridbox_config["login"]["password"] = PASSWORD
    logger.debug(gridbox_config["login"])
    one_time_print = True
    mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw, port=mqtt_port)
    viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)
    gridboxConnector = GridboxConnector(gridbox_config)
    while True:
        measurement = gridboxConnector.retrieve_live_data()
        if len(measurement) > 0:
            result = measurement[0]
            viessmann_gridbox_connector.update_sensors(result)
            if one_time_print or logger.level == logging.DEBUG:
                logger.info(result)
                one_time_print = False
            # Wait until fetch new values in seconds
        else:
            logger.warning("No data received")
            gridboxConnector.init_auth()
        time.sleep(WAIT)
