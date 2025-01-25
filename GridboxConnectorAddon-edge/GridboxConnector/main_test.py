import unittest
from unittest.mock import Mock, patch
from viessmann_gridbox_connector import GridboxConnector
import json
from ha_mqtt_discoverable import Settings
from ha_viessmann_gridbox_connector import HAViessmannGridboxConnector
from paho.mqtt.client import MQTT_ERR_SUCCESS
from ha_mqtt_discoverable.sensors import Sensor
os.environ['LOG_LEVEL'] = 'ERROR'
class TestGridboxConnectorMethods(unittest.TestCase):

    @patch('paho.mqtt.client.Client')
    @patch.object(GridboxConnector, 'init_auth', return_value=None)
    @patch.object(GridboxConnector, '__init__', return_value=None)
    @patch.object(GridboxConnector, 'retrieve_live_data')
    def test_main_batteries(self, mock_retrieve_live_data, mock_init, mock_init_auth,mock_mqtt_client):
        # Load mock data from JSON file
        with open('tests/mock_data/mock_data_with_batteries.json') as f:
            mock_data = [json.load(f)]
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_live_data.return_value = mock_data
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(
            host=mqtt_server, username=mqtt_user, password=mqtt_pw)
        viessmann_gridbox_connector = HAViessmannGridboxConnector(
            mqtt_settings)

        with patch.object(viessmann_gridbox_connector.self_supply_sensor, 'set_state') as mock_self_supply_sensor, \
             patch.object(viessmann_gridbox_connector.self_consumtion_rate_sensor, 'set_state') as mock_self_consumtion_rate_sensor, \
             patch.object(viessmann_gridbox_connector.consumption_household_sensor, 'set_state') as mock_consumption_household_sensor, \
             patch.object(viessmann_gridbox_connector.direct_consumption_household_sensor, 'set_state') as mock_direct_consumption_household_sensor, \
             patch.object(viessmann_gridbox_connector.direct_consumption_heatpump_sensor, 'set_state') as mock_direct_consumption_heatpump_sensor, \
             patch.object(viessmann_gridbox_connector.direct_consumption_rate_sensor, 'set_state') as mock_direct_consumption_rate_sensor, \
             patch.object(viessmann_gridbox_connector.battery_sum, 'set_states') as mock_battery_sum_sensor, \
             patch.object(viessmann_gridbox_connector.self_sufficiency_rate_sensor, 'set_state') as mock_self_sufficiency_rate_sensor:
            viessmann_gridbox_connector.update_sensors(result[0])
            mock_self_supply_sensor.assert_called_once_with(600.0, last_reset=None)
            mock_self_consumtion_rate_sensor.assert_called_once_with(96.1)
            mock_consumption_household_sensor.assert_called_once_with(600, last_reset=None)
            mock_direct_consumption_household_sensor.assert_called_once_with(600.0, last_reset=None)
            mock_direct_consumption_heatpump_sensor.assert_called_once_with(0.0, last_reset=None)
            mock_direct_consumption_rate_sensor.assert_called_once_with(39.68)
            mock_self_sufficiency_rate_sensor.assert_called_once_with(100.0)
            mock_battery_sum_sensor.assert_called_once_with(77.0, 10000.0, -853.0, 7700.0, -1.0, -1.0, None)

    @patch('paho.mqtt.client.Client')
    @patch.object(GridboxConnector, 'init_auth', return_value=None)
    @patch.object(GridboxConnector, '__init__', return_value=None)
    @patch.object(GridboxConnector, 'retrieve_live_data')
    def test_main_ev(self, mock_retrieve_live_data, mock_init, mock_init_auth,mock_mqtt_client):
        # Load mock data from JSON file
        with open('tests/mock_data/mock_data_with_ev.json') as f:
            mock_data = [json.load(f)]
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_live_data.return_value = mock_data
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(
            host=mqtt_server, username=mqtt_user, password=mqtt_pw)
        viessmann_gridbox_connector = HAViessmannGridboxConnector(
            mqtt_settings)

        with patch.object(viessmann_gridbox_connector.ev_sum, 'set_states') as mock_ev_sum:
            viessmann_gridbox_connector.update_sensors(result[0])
            mock_ev_sum.assert_called_once_with(7930.4,0,0,0,0,0)

    @patch('paho.mqtt.client.Client')
    @patch.object(GridboxConnector, 'init_auth', return_value=None)
    @patch.object(GridboxConnector, '__init__', return_value=None)
    @patch.object(GridboxConnector, 'retrieve_live_data')
    def test_main_heater(self, mock_retrieve_live_data, mock_init, mock_init_auth,mock_mqtt_client):
        # Load mock data from JSON file
        with open('tests/mock_data/mock_data_with_heater.json') as f:
            mock_data = [json.load(f)]
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_live_data.return_value = mock_data
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw)
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)

        with patch.object(viessmann_gridbox_connector.heater_sensor, 'set_states') as mock_heater_sensor:
            viessmann_gridbox_connector.update_sensors(result[0], last_reset=None)
            mock_heater_sensor.assert_called_once_with(3676,70.9)

    def test_logger(self):
        import os
        import logging
        from utils import SensitiveDataFilter
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO')))
        formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addFilter(SensitiveDataFilter())
        login_message = "{'grant_type': 'http://auth0.com/oauth/grant-type/password-realm', 'username': 'username@username', 'password': 'UltraSecret', 'audience': 'my.gridx', 'client_id': 'oZpr934Ikn8OZOHTJEcrgXkjio0I0Q7b', 'scope': 'email openid', 'realm': 'viessmann-authentication-db', 'client_secret': ''}"
        logger.info(login_message)

if __name__ == '__main__':
    unittest.main()
