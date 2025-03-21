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
    @patch.object(GridboxConnector, "retrieve_live_data")
    def test_main_batteries(
        self, mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client
    ):
        # Load mock data from JSON file
        with open("tests/mock_data/mock_data_with_batteries.json") as f:
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
            host=mqtt_server, username=mqtt_user, password=mqtt_pw
        )
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)

        with (
            patch.object(
                viessmann_gridbox_connector.self_supply_sensor, "set_state"
            ) as mock_self_supply_sensor,
            patch.object(
                viessmann_gridbox_connector.self_consumtion_rate_sensor, "set_state"
            ) as mock_self_consumtion_rate_sensor,
            patch.object(
                viessmann_gridbox_connector.consumption_household_sensor, "set_state"
            ) as mock_consumption_household_sensor,
            patch.object(
                viessmann_gridbox_connector.direct_consumption_household_sensor,
                "set_state",
            ) as mock_direct_consumption_household_sensor,
            patch.object(
                viessmann_gridbox_connector.direct_consumption_heatpump_sensor,
                "set_state",
            ) as mock_direct_consumption_heatpump_sensor,
            patch.object(
                viessmann_gridbox_connector.direct_consumption_rate_sensor, "set_state"
            ) as mock_direct_consumption_rate_sensor,
            patch.object(
                viessmann_gridbox_connector.battery_sum, "set_states"
            ) as mock_battery_sum_sensor,
            patch.object(
                viessmann_gridbox_connector.self_sufficiency_rate_sensor, "set_state"
            ) as mock_self_sufficiency_rate_sensor,
        ):
            viessmann_gridbox_connector.update_sensors(result[0])
            mock_self_supply_sensor.assert_called_once_with(600.0, last_reset=None)
            mock_self_consumtion_rate_sensor.assert_called_once_with(96.1)
            mock_consumption_household_sensor.assert_called_once_with(
                600, last_reset=None
            )
            mock_direct_consumption_household_sensor.assert_called_once_with(
                600.0, last_reset=None
            )
            mock_direct_consumption_heatpump_sensor.assert_called_once_with(
                0.0, last_reset=None
            )
            mock_direct_consumption_rate_sensor.assert_called_once_with(39.68)
            mock_self_sufficiency_rate_sensor.assert_called_once_with(100.0)
            mock_battery_sum_sensor.assert_called_once_with(
                77.0, 10000.0, -853.0, 7700.0, -1.0, -1.0, None
            )

    @patch("paho.mqtt.client.Client")
    @patch.object(GridboxConnector, "init_auth", return_value=None)
    @patch.object(GridboxConnector, "__init__", return_value=None)
    @patch.object(GridboxConnector, "retrieve_live_data")
    def test_main_ev(
        self, mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client
    ):
        # Load mock data from JSON file
        with open("tests/mock_data/mock_data_with_ev.json") as f:
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
            host=mqtt_server, username=mqtt_user, password=mqtt_pw
        )
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)

        with patch.object(
            viessmann_gridbox_connector.ev_sum, "set_states"
        ) as mock_ev_sum:
            viessmann_gridbox_connector.update_sensors(result[0])
            mock_ev_sum.assert_called_once_with(7930.4, 0, 0, 0, 0, 0)

    @patch("paho.mqtt.client.Client")
    @patch.object(GridboxConnector, "init_auth", return_value=None)
    @patch.object(GridboxConnector, "__init__", return_value=None)
    @patch.object(GridboxConnector, "retrieve_live_data")
    def test_main_heater(
        self, mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client
    ):
        # Load mock data from JSON file
        with open("tests/mock_data/mock_data_with_heater.json") as f:
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
            host=mqtt_server, username=mqtt_user, password=mqtt_pw
        )
        viessmann_gridbox_connector = HAViessmannGridboxConnector(mqtt_settings)

    @patch("paho.mqtt.client.Client")
    @patch.object(GridboxConnector, "init_auth", return_value=None)
    @patch.object(GridboxConnector, "__init__", return_value=None)
    @patch.object(GridboxConnector, "retrieve_historical_data")
    def test_main_historical_data(
        self, mock_retrieve_historical_data, mock_init, mock_init_auth, mock_mqtt_client
    ):
        # Load mock data from JSON file
        with open(
            "tests/mock_data/mock_data_historical_with_heater_and_battery.json"
        ) as f:
            mock_data = [json.load(f)]
        mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
        mock_retrieve_historical_data.return_value = mock_data

        from datetime import datetime, timezone, timedelta

        mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone(timedelta(hours=1)))
        mock_now = mock_now.replace(hour=0, minute=0, second=0, microsecond=0)
        today = mock_now.isoformat()
        tomorrow = (mock_now + timedelta(days=1)).isoformat()
        midnight_today = mock_now.replace(hour=0, minute=0, second=0, microsecond=0)
        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_historical_data(today, tomorrow)

        # Assert the function was called once
        mock_retrieve_historical_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)
        mqtt_server = "mqtt_server"
        mqtt_user = "mqtt_user"
        mqtt_pw = "mqtt_pw"
        mqtt_settings = Settings.MQTT(
            host=mqtt_server, username=mqtt_user, password=mqtt_pw
        )
        viessmann_gridbox_historical_device = HAViessmannGridboxConnector(
            mqtt_settings=mqtt_settings,
            device_name="Viessmann Gridbox Historical",
            device_identifiers="viessmann_gridbox_historical",
            prefix="historical",
            unit_of_power="Wh",
            device_class_of_power="energy",
            state_class="total",
        )

        with (
            patch.object(
                viessmann_gridbox_historical_device.battery_sum, "set_states"
            ) as mock_battery_sum_sensor,
            patch.object(
                viessmann_gridbox_historical_device.feed_in_sensor, "set_state"
            ) as mock_feed_in_sensor,
        ):
            viessmann_gridbox_historical_device.update_sensors(
                result[0], last_reset=midnight_today.isoformat()
            )
            mock_battery_sum_sensor.assert_called_once_with(
                3.3195323553890965,
                6354.166666666667,
                0.0,
                0.0,
                548.55,
                3612.91,
                "2023-01-01T00:00:00+01:00",
            )
            mock_feed_in_sensor.assert_called_once_with(
                55.148500000000006, last_reset="2023-01-01T00:00:00+01:00"
            )
        self.assertIsNotNone(viessmann_gridbox_historical_device.feed_in_sensor)
        # self.assertIsNone(viessmann_gridbox_historical_device.grid_sensor)

    def test_logger(self):
        import os
        import logging
        from utils import SensitiveDataFilter

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
        formatter = logging.Formatter(
            "%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addFilter(SensitiveDataFilter())
        login_message = "{'grant_type': 'http://auth0.com/oauth/grant-type/password-realm', 'username': 'username@username', 'password': 'UltraSecret', 'audience': 'my.gridx', 'client_id': 'oZpr934Ikn8OZOHTJEcrgXkjio0I0Q7b', 'scope': 'email openid', 'realm': 'viessmann-authentication-db', 'client_secret': ''}"
        # logger.info(login_message)


if __name__ == "__main__":
    unittest.main()
