from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from ha_mqtt_discoverable import Settings, DeviceInfo
import logging

class HAViessmannBattery:
    """
The Battery class represents a battery with associated sensors for level, capacity, power, and remaining charge. Each sensor is created as an MQTT entity with its own SensorInfo and Settings.

Attributes:
    id (str): The unique ID of the battery.
    name (str): The name of the battery.
    device_info (DeviceInfo): The device information of the battery.
    mqtt_settings (Settings.MQTT): The MQTT settings for the sensors.
    battery_level (Sensor): The sensor for the battery level.
    battery_capacity (Sensor): The sensor for the battery capacity.
    battery_power (Sensor): The sensor for the battery power.
    battery_remaining_charge (Sensor): The sensor for the remaining battery charge.

Methods:
    get_name(): Returns the name of the battery.
    set_states(level, capacity, power, remaining_charge): Sets the states of the four sensors.
"""

    def __init__(self, mqtt_settings, device_info, name, id,logger=logging.getLogger(__name__), prefix="", unit_of_power="W", state_class=None):
        self.id: str = id
        self.name: str = name
        self.device_info: DeviceInfo = device_info
        self.mqtt_settings: Settings.MQTT = mqtt_settings
        self.logger: logging.Logger = logger
        self.prefix: str = prefix
        self.unit_of_power: str = unit_of_power
        self.state_class: str = state_class
        self.battery_charge = None
        self.battery_discharge = None

        self.battery_sensor_info = SensorInfo(name=f"Battery {name} Level", device_class="battery", unique_id=f"gridbox_battery_{name}"+prefix, device=device_info, unit_of_measurement="%")
        self.battery_settings = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_info)
        self.battery_level = Sensor(self.battery_settings)

        self.battery_sensor_capacity = SensorInfo(name=f"Battery {name} Capacity", device_class="energy", unique_id=f"gridbox_battery_level_{name}"+prefix, device=device_info, unit_of_measurement="Wh", state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        self.battery_settings_capacity = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_capacity)
        self.battery_capacity = Sensor(self.battery_settings_capacity)

        self.battery_sensor_power = SensorInfo(name=f"Battery {name} Power", device_class="battery", unique_id=f"gridbox_battery_power_{name}"+prefix, device=device_info, unit_of_measurement=unit_of_power, state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        self.battery_settings_power = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_power)
        self.battery_power = Sensor(self.battery_settings_power)

        self.battery_sensor_remaining_charge = SensorInfo(name=f"Battery {name} Remaining Charge", device_class="energy", unique_id=f"gridbox_remaining_charge_{name}"+prefix, device=device_info, unit_of_measurement="Wh", state_class=state_class, value_template=None if state_class is None else "{{ value_json.state }}", last_reset_value_template=None if state_class is None else "{{ value_json.last_reset }}")
        self.battery_settings_remaining_charge = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_remaining_charge)
        self.battery_remaining_charge = Sensor(self.battery_settings_remaining_charge)



    def get_name(self):
        return self.name

    def set_states(self, level, capacity, power, remaining_charge, charge=-1, discharge=-1, last_reset=None):
        self.battery_level.set_state(level)
        self.battery_capacity.set_state(capacity)
        self.battery_power.set_state(power)
        self.battery_remaining_charge.set_state(remaining_charge)
        if charge == -1 and discharge == -1:
            charge = 1000
            discharge = 1000
        try:
            if charge >= 0 and self.battery_charge is None:
                self.battery_sensor_charge = SensorInfo(name=f"Battery {self.name} Charge", device_class="energy", unique_id=f"gridbox_charge_{self.name}"+self.prefix, device=self.device_info, unit_of_measurement="Wh", state_class=self.state_class, value_template=None if self.state_class is None else "{{ value_json.state }}", last_reset_value_template=None if self.state_class is None else "{{ value_json.last_reset }}")
                self.battery_settings_charge = Settings(mqtt=self.mqtt_settings, entity=self.battery_sensor_charge)
                self.battery_charge = Sensor(self.battery_settings_charge)
            if charge >= 0 and self.battery_charge is not None:
                self.battery_charge.set_state(charge, last_reset)
        except Exception as e:
            self.logger.error(f"Error setting charge state: {e}")
        try:

            if discharge >= 0 and self.battery_discharge is None:
                self.battery_sensor_discharge = SensorInfo(name=f"Battery {self.name} Discharge", device_class="energy", unique_id=f"gridbox_discharge_{self.name}"+self.prefix, device=self.device_info, unit_of_measurement="Wh", state_class=self.state_class, value_template=None if self.state_class is None else "{{ value_json.state }}", last_reset_value_template=None if self.state_class is None else "{{ value_json.last_reset }}")
                self.battery_settings_discharge = Settings(mqtt=self.mqtt_settings, entity=self.battery_sensor_discharge)
                self.battery_discharge = Sensor(self.battery_settings_discharge)
            if discharge >= 0 and self.battery_discharge is not None:
                self.battery_discharge.set_state(discharge, last_reset)
        except Exception as e:
            self.logger.error(f"Error setting discharge state: {e}")