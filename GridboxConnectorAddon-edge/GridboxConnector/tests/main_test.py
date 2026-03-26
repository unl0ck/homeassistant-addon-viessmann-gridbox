import os
import logging
import pytest
from unittest.mock import patch
from gridx_connector import GridboxConnector
from ha_gridbox_connector import HAGridboxConnector
from paho.mqtt.client import MQTT_ERR_SUCCESS
from conftest import load_mock_data


def _make_connector(mock_retrieve_live_data, mock_mqtt_client, filename):
    mock_mqtt_client.return_value.connect.return_value = MQTT_ERR_SUCCESS
    mock_data = load_mock_data(filename)
    mock_retrieve_live_data.return_value = mock_data
    connector = GridboxConnector(None)
    result = connector.retrieve_live_data_by_id()
    mock_retrieve_live_data.assert_called_once()
    assert result == mock_data
    return result


@patch("paho.mqtt.client.Client")
@patch.object(GridboxConnector, "init_auth", return_value=None)
@patch.object(GridboxConnector, "__init__", return_value=None)
@patch.object(GridboxConnector, "retrieve_live_data_by_id")
def test_main_batteries(mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client, mqtt_settings):
    result = _make_connector(mock_retrieve_live_data, mock_mqtt_client, "mock_data_with_batteries.json")
    ha = HAGridboxConnector(mqtt_settings)
    ha.update_sensors(result)
    with (
        patch.object(ha.production, "set_state") as mock_production,
        patch.object(ha.selfConsumptionRate, "set_state") as mock_self_consumption_rate,
    ):
        ha.update_sensors(result)
        mock_production.assert_called_once_with(1512, last_reset="")
        mock_self_consumption_rate.assert_called_once_with(96.1, last_reset="")


@patch("paho.mqtt.client.Client")
@patch.object(GridboxConnector, "init_auth", return_value=None)
@patch.object(GridboxConnector, "__init__", return_value=None)
@patch.object(GridboxConnector, "retrieve_live_data_by_id")
def test_main_ev(mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client, mqtt_settings):
    result = _make_connector(mock_retrieve_live_data, mock_mqtt_client, "mock_data_with_ev.json")
    ha = HAGridboxConnector(mqtt_settings)
    ha.update_sensors(result)
    with patch.object(ha.evChargingStation_power, "set_state") as mock_ev_power:
        ha.update_sensors(result)
        mock_ev_power.assert_called_once_with(7930.4, last_reset="")


@patch("paho.mqtt.client.Client")
@patch.object(GridboxConnector, "init_auth", return_value=None)
@patch.object(GridboxConnector, "__init__", return_value=None)
@patch.object(GridboxConnector, "retrieve_live_data_by_id")
def test_main_heater(mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client, mqtt_settings):
    result = _make_connector(mock_retrieve_live_data, mock_mqtt_client, "mock_data_with_heater.json")
    ha = HAGridboxConnector(mqtt_settings)
    ha.update_sensors(result)
    with (
        patch.object(ha.heaters_power, "set_state") as mock_heaters_power,
        patch.object(ha.heaters_temperature, "set_state") as mock_heaters_temperature,
    ):
        ha.update_sensors(result)
        mock_heaters_power.assert_called_once_with(3676, last_reset="")
        mock_heaters_temperature.assert_called_once_with(70.9, last_reset="")


@patch("paho.mqtt.client.Client")
@patch.object(GridboxConnector, "init_auth", return_value=None)
@patch.object(GridboxConnector, "__init__", return_value=None)
@patch.object(GridboxConnector, "retrieve_live_data_by_id")
def test_main_heatpump(mock_retrieve_live_data, mock_init, mock_init_auth, mock_mqtt_client, mqtt_settings):
    result = _make_connector(mock_retrieve_live_data, mock_mqtt_client, "mock_data_with_heatpump.json")
    ha = HAGridboxConnector(mqtt_settings)
    ha.update_sensors(result)
    with (
        patch.object(ha.heatPumps_power, "set_state") as mock_heatpumps_power,
        patch.object(ha.heatPumps_sgReadyState, "set_state") as mock_heatpumps_sg_ready_state,
    ):
        ha.update_sensors(result)
        mock_heatpumps_power.assert_called_once_with(1074.93, last_reset="")
        mock_heatpumps_sg_ready_state.assert_called_once_with("AUTO")


def test_logger():
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
