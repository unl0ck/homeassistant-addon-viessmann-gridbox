import unittest
from unittest.mock import Mock, patch
from viessmann_gridbox_connector import GridboxConnector
import json
from ha_mqtt_discoverable import Settings
from ha_viessmann_gridbox_connector import HAViessmannGridboxConnector
from paho.mqtt.client import MQTT_ERR_SUCCESS
from ha_mqtt_discoverable.sensors import Sensor

mock_data = "{'batteries': [{'applianceID': '97af25d0-3791-48cc-857c-14aaac749267', 'capacity': 10000, 'nominalCapacity': 10000, 'power': -853, 'remainingCharge': 7700, 'stateOfCharge': 0.77}], 'battery': {'capacity': 10000, 'nominalCapacity': 10000, 'power': -853, 'remainingCharge': 7700, 'stateOfCharge': 0.77}, 'consumption': 600, 'directConsumption': 600, 'directConsumptionEV': 0, 'directConsumptionHeatPump': 0, 'directConsumptionHeater': 0, 'directConsumptionHousehold': 600, 'directConsumptionRate': 0.3968253968253968, 'grid': -59, 'gridMeterReadingNegative': 14081760000, 'gridMeterReadingPositive': 7393320000, 'measuredAt': '2024-05-08T09:42:18Z', 'photovoltaic': 1512, 'production': 1512, 'selfConsumption': 1453, 'selfConsumptionRate': 0.9609788359788359, 'selfSufficiencyRate': 1, 'selfSupply': 600, 'totalConsumption': 600}"


class TestGridboxConnectorMethods(unittest.TestCase):

    @patch('paho.mqtt.client.Client')
    @patch.object(GridboxConnector, 'init_auth', return_value=None)
    @patch.object(GridboxConnector, '__init__', return_value=None)
    @patch.object(GridboxConnector, 'retrieve_live_data')
    def test_main(self, mock_retrieve_live_data, mock_init, mock_init_auth,mock_mqtt_client):
        # Load mock data from JSON file
        with open('tests/mock_data/mock_data_with_batteries.json') as f:
            mock_data = json.load(f)
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
             patch.object(viessmann_gridbox_connector.direct_consumption_heatpump_sensor, 'set_state') as mock_direct_consumtion_heatpump_sensor, \
             patch.object(viessmann_gridbox_connector.direct_consumption_rate_sensor, 'set_state') as mock_direct_consumtion_rate_sensor, \
             patch.object(viessmann_gridbox_connector.self_sufficiency_rate_sensor, 'set_state') as mock_self_sufficiency_rate_sensor:
            viessmann_gridbox_connector.update_sensors(result[0])
            mock_self_supply_sensor.assert_called_once_with(600.0)
            mock_self_consumtion_rate_sensor.assert_called_once_with(96.09788359788359)
            mock_consumption_household_sensor.assert_called_once_with(600)
            mock_direct_consumption_household_sensor.assert_called_once_with(600.0)
            mock_direct_consumtion_heatpump_sensor.assert_called_once_with(0.0)
            mock_direct_consumtion_rate_sensor.assert_called_once_with(39.682539682539684)
            mock_self_sufficiency_rate_sensor.assert_called_once_with(100.0)
        
if __name__ == '__main__':
    unittest.main()
