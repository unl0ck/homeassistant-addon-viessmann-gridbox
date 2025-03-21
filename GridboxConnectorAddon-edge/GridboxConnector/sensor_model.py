from pydantic import BaseModel
from typing import Optional
from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
import json


class SensorModel(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    device_class: Optional[str] = None
    factor: Optional[int] = None
    unique_id: Optional[str] = None
    state_class: Optional[str] = None
    value_template: Optional[str] = None
    last_reset_value_template: Optional[str] = None


def load_sensor_by_key(key: str, path: str = "models/models.json", type: str = "base") -> SensorModel:
    with open(path) as f:
        sensors: dict = json.load(f)
        type_json = sensors.get(type, None)
        if type_json is None:
            raise ValueError(f"Type {key} not found")
        sensor_json = type_json.get(key, None)
        if sensor_json is None:
            raise ValueError(f"Sensor {key} not found")
    return SensorModel.model_validate(sensor_json)


def key_in_model(key: str, path: str = "models/models.json", type: str = "base") -> bool:
    with open(path) as f:
        sensors: dict = json.load(f)
        type_json = sensors.get(type, None)
        if type_json is None:
            return False
        return key in type_json


def create_ha_sensor(key: str, device_info: DeviceInfo, mqtt_settings: Settings.MQTT, type: str = "base", path: str = "models/models.json") -> Sensor:
    sensor: SensorModel = load_sensor_by_key(key, type=type, path=path)
    sensor_info = SensorInfo(
        name=sensor.name,
        device_class=sensor.device_class,
        unique_id=f"{device_info.identifiers}_{sensor.unique_id}",
        device=device_info,
        unit_of_measurement=sensor.unit,
        state_class=sensor.state_class,
        value_template=sensor.value_template,
        last_reset_value_template=sensor.last_reset_value_template,
    )
    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    return Sensor(settings)


if __name__ == "__main__":
    print(repr(load_sensor_by_key("production")))
    with open("tests/mock_data/mock_data_with_batteries.json") as f:
        mock_data = json.load(f)
        for key, value in mock_data.items():
            try:
                print(repr(load_sensor_by_key(key)))
            except ValueError as e:
                print(e)
                continue
    with open("tests/mock_data/mock_data_with_batteries.json") as f:
        mock_data = json.load(f)
        for key, value in mock_data.items():
            try:
                print(repr(load_sensor_by_key(key=key, path="models/models_historical.json")))
            except ValueError as e:
                print(e)
                continue
