from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from ha_mqtt_discoverable import Settings

class Battery:
    def __init__(self, mqtt_settings, device_info, name, id):
        self.id = id
        self.name = name
        self.device_info = device_info
        self.mqtt_settings = mqtt_settings
        
        self.battery_sensor_info = SensorInfo(name=f"Battery {name} Level", device_class="battery", unique_id=f"gridbox_battery_{name}", device=device_info, unit_of_measurement="%")
        self.battery_settings = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_info)
        self.battery_level = Sensor(self.battery_settings)
        
        self.battery_sensor_capacity = SensorInfo(name=f"Battery {name} Capacity", device_class="energy", unique_id=f"gridbox_battery_level_{name}", device=device_info, unit_of_measurement="Wh")
        self.battery_settings_capacity = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_capacity)
        self.battery_capacity = Sensor(self.battery_settings_capacity)
        
        self.battery_sensor_power = SensorInfo(name=f"Battery {name} Power", device_class="battery", unique_id=f"gridbox_battery_power_{name}", device=device_info, unit_of_measurement="W")
        self.battery_settings_power = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_power)
        self.battery_power = Sensor(self.battery_settings_power)

        self.battery_sensor_remaining_charge = SensorInfo(name=f"Battery {name} Remaining Charge", device_class="energy", unique_id=f"gridbox_remaining_charge_{name}", device=device_info, unit_of_measurement="Wh")
        self.battery_settings_remaining_charge = Settings(mqtt=mqtt_settings, entity=self.battery_sensor_remaining_charge)
        self.battery_remaining_charge = Sensor(self.battery_settings_remaining_charge)
    
    def get_name(self):
        return self.name
    
    def set_states(self, level, capacity, power, remaining_charge):
        self.battery_level.set_state(level)
        self.battery_capacity.set_state(capacity)
        self.battery_power.set_state(power)
        self.battery_remaining_charge.set_state(remaining_charge)