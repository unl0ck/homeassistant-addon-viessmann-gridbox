# Home Assistant Add-on: GridboxConnector

Fetch your Energy data from the Viessmann Gridbox Cloud

## How to use

### Prerequisite

Installed and Setup MQTT-Broker

### Configuration

Enter your Gridbox Credentials in the Configuration
use your credentials from the Viessmann **myGridbox** App or from the Viessmann Gridbox Webseite https://mygridbox.viessmann.com/login

```yml
username: email
password: password
wait_time: timeout when will refresh
OverrideMqttUser: Mqtt user
OverrideMqttPw: Mqtt password
OverrideMqttServer: Mqtt Server
OverrideMqttPort: Mqtt Port
log_level: select one of this(TRACE|DEBUG|INFO|WARN|ERROR)
enable_telemetry: Send to logfire logs and exceptions
```

if you use an custom setup MQTT-Broker so you can add in the Addon the MQTT settings currently only support MQTT Standard Port 1833 (will fixed later)

_Remember you have to restart the Addon after changed the Credentials_

### Result

If you setup your correct credentials you will see

![GridboxConnector Result](images/sensor_overview.png)
