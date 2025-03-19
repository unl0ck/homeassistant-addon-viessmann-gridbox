from pydantic import BaseModel
from typing import Optional
from pydantic_core import from_json
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


if __name__ == "__main__":
    print(repr(load_sensor_by_key("production")))
    with open('tests/mock_data/mock_data_with_batteries.json') as f:
        mock_data = json.load(f)
        for key, value in mock_data.items():
            try:
                print(repr(load_sensor_by_key(key)))
            except ValueError as e:
                print(e)
                continue
    with open('tests/mock_data/mock_data_with_batteries.json') as f:
        mock_data = json.load(f)
        for key, value in mock_data.items():
            try:
                print(repr(load_sensor_by_key(key=key, path="models/models_historical.json")))
            except ValueError as e:
                print(e)
                continue
