from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Sensor, SensorInfo


class HAViessmannEVChargingStation:
    appliance_id: str
    power_sensor: Sensor
    state_of_charge: Sensor
    plug_state: Sensor
    current_l1: Sensor
    current_l2: Sensor
    current_l3: Sensor
    reading_total: Sensor
    name: str
    device_info: DeviceInfo
    mqtt_settings: Settings.MQTT

    def __init__(self, mqtt_settings, device_info, name, appliance_id):
        self.appliance_id = appliance_id
        self.name = name
        self.device_info = device_info
        self.mqtt_settings = mqtt_settings

        self.power_sensor_info = SensorInfo(name=f"{name} Power", device_class="power", unique_id=f"gridbox_ev_charging_station_power_{name}", device=device_info, unit_of_measurement="W")
        self.power_settings = Settings(mqtt=mqtt_settings, entity=self.power_sensor_info)
        self.power_sensor = Sensor(self.power_settings)

        self.state_of_charge_sensor_info = SensorInfo(
            name=f"{name} State of Charge", device_class="battery", unique_id=f"gridbox_ev_charging_station_state_of_charge_{name}", device=device_info, unit_of_measurement="%"
        )
        self.state_of_charge_settings = Settings(mqtt=mqtt_settings, entity=self.state_of_charge_sensor_info)
        self.state_of_charge = Sensor(self.state_of_charge_settings)

        self.plug_state_sensor_info = SensorInfo(name=f"{name} Plug State", device_class="plug", unique_id=f"gridbox_ev_charging_station_plug_state_{name}", device=device_info)
        self.plug_state_settings = Settings(mqtt=mqtt_settings, entity=self.plug_state_sensor_info)
        self.plug_state = Sensor(self.plug_state_settings)

        self.current_l1_sensor_info = SensorInfo(
            name=f"{name} Current L1", device_class="current", unique_id=f"gridbox_ev_charging_station_current_l1_{name}", device=device_info, unit_of_measurement="A"
        )
        self.current_l1_settings = Settings(mqtt=mqtt_settings, entity=self.current_l1_sensor_info)
        self.current_l1 = Sensor(self.current_l1_settings)

        self.current_l2_sensor_info = SensorInfo(
            name=f"{name} Current L2", device_class="current", unique_id=f"gridbox_ev_charging_station_current_l2_{name}", device=device_info, unit_of_measurement="A"
        )
        self.current_l2_settings = Settings(mqtt=mqtt_settings, entity=self.current_l2_sensor_info)
        self.current_l2 = Sensor(self.current_l2_settings)

        self.current_l3_sensor_info = SensorInfo(
            name=f"{name} Current L3", device_class="current", unique_id=f"gridbox_ev_charging_station_current_l3_{name}", device=device_info, unit_of_measurement="A"
        )
        self.current_l3_settings = Settings(mqtt=mqtt_settings, entity=self.current_l3_sensor_info)
        self.current_l3 = Sensor(self.current_l3_settings)

        self.reading_total_sensor_info = SensorInfo(
            name=f"{name} Reading Total", device_class="energy", unique_id=f"gridbox_ev_charging_station_reading_total_{name}", device=device_info, unit_of_measurement="Wh"
        )
        self.reading_total_settings = Settings(mqtt=mqtt_settings, entity=self.reading_total_sensor_info)
        self.reading_total = Sensor(self.reading_total_settings)

    def set_states(self, power, state_of_charge, current_l1, current_l2, current_l3, reading_total):
        self.power_sensor.set_state(power)
        self.state_of_charge.set_state(state_of_charge)
        self.current_l1.set_state(current_l1)
        self.current_l2.set_state(current_l2)
        self.current_l3.set_state(current_l3)
        self.reading_total.set_state(reading_total)
