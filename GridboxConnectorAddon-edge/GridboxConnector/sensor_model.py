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
    last_reset_topic: Optional[str] = None


def load_sensor_by_key(key: str) -> SensorModel:
    with open('models.json') as f:
        sensors: dict = json.load(f)
        sensor_json_value = sensors.get(key, None)
        if sensor_json_value is None:
            raise ValueError(f"Sensor with key {key} not found")
        sensor = json.dumps(sensors.get(key))
    return SensorModel.model_validate(from_json(sensor))


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
