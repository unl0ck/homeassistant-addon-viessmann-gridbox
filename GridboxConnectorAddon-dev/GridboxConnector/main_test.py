import unittest
from unittest.mock import Mock, patch
from gridbox_connector import GridboxConnector
import json

mock_data = "{'batteries': [{'applianceID': '97af25d0-3791-48cc-857c-14aaac749267', 'capacity': 10000, 'nominalCapacity': 10000, 'power': -853, 'remainingCharge': 7700, 'stateOfCharge': 0.77}], 'battery': {'capacity': 10000, 'nominalCapacity': 10000, 'power': -853, 'remainingCharge': 7700, 'stateOfCharge': 0.77}, 'consumption': 600, 'directConsumption': 600, 'directConsumptionEV': 0, 'directConsumptionHeatPump': 0, 'directConsumptionHeater': 0, 'directConsumptionHousehold': 600, 'directConsumptionRate': 0.3968253968253968, 'grid': -59, 'gridMeterReadingNegative': 14081760000, 'gridMeterReadingPositive': 7393320000, 'measuredAt': '2024-05-08T09:42:18Z', 'photovoltaic': 1512, 'production': 1512, 'selfConsumption': 1453, 'selfConsumptionRate': 0.9609788359788359, 'selfSufficiencyRate': 1, 'selfSupply': 600, 'totalConsumption': 600}"


class TestGridboxConnectorMethods(unittest.TestCase):

    @ patch.object(GridboxConnector, 'init_auth', return_value=None)
    @ patch.object(GridboxConnector, '__init__', return_value=None)
    @ patch.object(GridboxConnector, 'retrieve_live_data', return_value=mock_data)
    def test_main(self, mock_retrieve_live_data, mock_init, mock_init_auth):
        # Create an instance of the class
        gridbox_connector = GridboxConnector(None)

        # Call the function
        result = gridbox_connector.retrieve_live_data()

        # Assert the function was called once
        mock_retrieve_live_data.assert_called_once()

        # Assert the function returned the mock value
        self.assertEqual(result, mock_data)


if __name__ == '__main__':
    unittest.main()
