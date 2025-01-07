from pydantic import BaseModel
from typing import Optional, List
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
        sensors = json.load(f)
        sensor = json.dumps(sensors.get(key))
    return SensorModel.model_validate(from_json(sensor))
