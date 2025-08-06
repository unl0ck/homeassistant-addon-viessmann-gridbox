from ha_mqtt_discoverable.sensors import Sensor, SensorInfo
from ha_mqtt_discoverable import Settings, DeviceInfo


class HAViessmannHeater:
    def __init__(self, mqtt_settings, device_info, name, id, prefix=""):
        self.id: str = id
        self.name: str = name
        self.device_info: DeviceInfo = device_info
        self.mqtt_settings: Settings.MQTT = mqtt_settings

        self.heater_sensor_power = SensorInfo(
            name=f"Heater {name} Power", device_class="power", unique_id=f"gridbox_heater_power_{name}"+prefix, device=device_info, unit_of_measurement="W")
        self.heater_power_settings = Settings(
            mqtt=mqtt_settings, entity=self.heater_sensor_power)
        self.heater_power = Sensor(self.heater_power_settings)

        self.heater_sensor_temperature = SensorInfo(
            name=f"Heater {name} Temperature", device_class="temperature", unique_id=f"gridbox_heater_temperature_{name}"+prefix, device=device_info, unit_of_measurement="°C")
        self.heater_temperature_settings = Settings(
            mqtt=mqtt_settings, entity=self.heater_sensor_temperature)
        self.heater_temperature = Sensor(self.heater_temperature_settings)


    def get_name(self):
        return self.name

    def set_states(self, power, temperature):
        self.heater_power.set_state(power)
        self.heater_temperature.set_state(temperature)

