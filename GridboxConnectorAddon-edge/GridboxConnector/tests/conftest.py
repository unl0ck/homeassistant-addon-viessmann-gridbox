import json
import pytest
from pathlib import Path
from ha_mqtt_discoverable import Settings


@pytest.fixture
def mqtt_settings():
    return Settings.MQTT(host="mqtt_server", username="mqtt_user", password="mqtt_pw")


def load_mock_data(filename):
    with open(Path(__file__).parent / "mock_data" / filename) as f:
        return json.load(f)
