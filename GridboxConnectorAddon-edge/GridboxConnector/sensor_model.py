from pydantic import BaseModel
from typing import Optional, List
import json

class Sensor(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    device_class: Optional[str] = None
    factor: Optional[int] = None
    unique_id: Optional[str] = None
    state_class: Optional[str] = None
    value_template: Optional[str] = None
    last_reset_topic: Optional[str] = None
