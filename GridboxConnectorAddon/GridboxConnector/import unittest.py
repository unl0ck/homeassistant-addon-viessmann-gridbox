import unittest
import logging
from unittest.mock import Mock, patch
from .utils import SensitiveDataFilter, get_bool_env

# FILE: GridboxConnectorAddon-edge/GridboxConnector/test_utils.py


class TestSensitiveDataFilter(unittest.TestCase):
    def setUp(self):
        self.filter = SensitiveDataFilter()

    def test_filter(self):
        record = logging.LogRecord(name="test", level=logging.INFO, pathname="", lineno=0, msg='{"username": "user", "password": "pass"}', args=(), exc_info=None)
        self.filter.filter(record)
        self.assertIn('"username": "***"', record.msg)
        self.assertIn('"password": "***"', record.msg)

    def test_filter_no_sensitive_data(self):
        record = logging.LogRecord(name="test", level=logging.INFO, pathname="", lineno=0, msg='{"data": "value"}', args=(), exc_info=None)
        self.filter.filter(record)
        self.assertIn('"data": "value"', record.msg)

    def test_filter_invalid_json(self):
        record = logging.LogRecord(name="test", level=logging.INFO, pathname="", lineno=0, msg='Invalid JSON', args=(), exc_info=None)
        self.filter.filter(record)
        self.assertEqual(record.msg, 'Invalid JSON')

class TestGetBoolEnv(unittest.TestCase):
    @patch('os.getenv', return_value="true")
    def test_get_bool_env_true(self, mock_getenv):
        self.assertTrue(get_bool_env("TEST_VAR"))

    @patch('os.getenv', return_value="false")
    def test_get_bool_env_false(self, mock_getenv):
        self.assertFalse(get_bool_env("TEST_VAR"))

    @patch('os.getenv', return_value=None)
    def test_get_bool_env_default(self, mock_getenv):
        self.assertFalse(get_bool_env("TEST_VAR"))

    @patch('os.getenv', return_value="1")
    def test_get_bool_env_one(self, mock_getenv):
        self.assertTrue(get_bool_env("TEST_VAR"))

    @patch('os.getenv', return_value="0")
    def test_get_bool_env_zero(self, mock_getenv):
        self.assertFalse(get_bool_env("TEST_VAR"))

if __name__ == '__main__':
    unittest.main()