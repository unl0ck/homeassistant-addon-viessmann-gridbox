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
```

if you use an custom setup MQTT-Broker so you can add in the Addon the MQTT settings currently only support MQTT Standard Port 1833 (will fixed later)

_Remember you have to restart the Addon after changed the Credentials_

### Result

If you setup your correct credentials you will see

![GridboxConnector Result](images/sensor_overview.png)
