import unittest
from unittest.mock import Mock, patch
from viessmann_gridbox_connector import GridboxConnector
import json
from ha_mqtt_discoverable import Settings
from ha_viessmann_gridbox_connector import HAViessmannGridboxConnector
from paho.mqtt.client import MQTT_ERR_SUCCESS
from ha_mqtt_discoverable.sensors import Sensor


class TestGridboxConnectorMethods(unittest.TestCase):
    @patch("paho.mqtt.client.Client")
    @patch.object(GridboxConnector, "init_auth", return_value=None)
    @patch.object(GridboxConnector, "__init__", return_value=None)
    @patch.object(GridboxConnector, "retrieve_live_data_by_id")
    def test_main_batteries(self, mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client):
        # Load mock data from JSON file
        with open("tests/mock_data/mock_data_with_batteries.json") as f:
            mock_data = json.load(f)
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_live_data.return_value = mock_data
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data_by_id()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw)
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)
        viessmann_gridbox_connector.update_sensors(result)
        with (
            patch.object(viessmann_gridbox_connector.production, "set_state") as mock_production,
            patch.object(viessmann_gridbox_connector.selfConsumptionRate, "set_state") as mock_self_consumtion_rate_sensor,
        ):
            viessmann_gridbox_connector.update_sensors(result)
            mock_production.assert_called_once_with(1512, last_reset=None)
            mock_self_consumtion_rate_sensor.assert_called_once_with(96.1, last_reset=None)

    @patch("paho.mqtt.client.Client")
    @patch.object(GridboxConnector, "init_auth", return_value=None)
    @patch.object(GridboxConnector, "__init__", return_value=None)
    @patch.object(GridboxConnector, "retrieve_live_data_by_id")
    def test_main_ev(self, mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client):
        # Load mock data from JSON file
        with open("tests/mock_data/mock_data_with_ev.json") as f:
            mock_data = json.load(f)
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_live_data.return_value = mock_data
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data_by_id()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw)
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)

        viessmann_gridbox_connector.update_sensors(result)
        with (
            patch.object(viessmann_gridbox_connector.evChargingStation_power, "set_state") as mock_evChargingStation_power,
        ):
            viessmann_gridbox_connector.update_sensors(result)
            mock_evChargingStation_power.assert_called_once_with(7930.4, last_reset=None)

    @patch("paho.mqtt.client.Client")
    @patch.object(GridboxConnector, "init_auth", return_value=None)
    @patch.object(GridboxConnector, "__init__", return_value=None)
    @patch.object(GridboxConnector, "retrieve_live_data_by_id")
    def test_main_heater(self, mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client):
        # Load mock data from JSON file
        with open("tests/mock_data/mock_data_with_heater.json") as f:
            mock_data = json.load(f)
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_live_data.return_value = mock_data
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data_by_id()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(host=mqtt_server, username=mqtt_user, password=mqtt_pw)
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)
        viessmann_gridbox_connector.update_sensors(result)
        with (
            patch.object(viessmann_gridbox_connector.heaters_power, "set_state") as mock_heaters_power,
            patch.object(viessmann_gridbox_connector.heaters_temperature, "set_state") as mock_heaters_temperature,
        ):
            viessmann_gridbox_connector.update_sensors(result)
            mock_heaters_power.assert_called_once_with(3676, last_reset=None)
            mock_heaters_temperature.assert_called_once_with(70.9, last_reset=None)

    def test_logger(self):
        import os
        import logging
        from utils import SensitiveDataFilter

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
        formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addFilter(SensitiveDataFilter())
        login_message = "{'grant_type': 'http://auth0.com/oauth/grant-type/password-realm', 'username': 'username@username', 'password': 'UltraSecret', 'audience': 'my.gridx', 'client_id': 'oZpr934Ikn8OZOHTJEcrgXkjio0I0Q7b', 'scope': 'email openid', 'realm': 'viessmann-authentication-db', 'client_secret': ''}"
        logger.info(login_message)


if __name__ == "__main__":
    unittest.main()
