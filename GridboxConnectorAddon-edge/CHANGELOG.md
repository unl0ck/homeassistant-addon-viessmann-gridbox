<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 2.11.18

### 🔨 Fixed

- historical data now support Wh

## 2.11.17

### 🔨 Fixed

- Worked on create new device and fixed hopefully
- Removed Telemetry

## 2.11.11

### 🚀 Added

- Historical Data Device

### 🔨 Fixed

- bump viessmann-gridbox-connector to 1.6.0
- bump ha-mqtt-discoverable to 0.16.0

## 2.10.0

### 🚀 Added

- Opentelemetry Class to collect exceptions

## 2.9.0

### 🔨 Fixed

- bump viessmann-connector to 1.5.1

## 2.8.5

### 🔨 Fixed

- restart Addon detection working

## 2.8.4

### 🚀 Added

- sensitive filter

## 2.8.0

### 🚀 Added

- Heaters with Temperature and power

### 🔨 Fixed

- does not show anymore credentials in log

## 2.7.6

### 🔨 Fixed

- if list of values is empty refresh token

## 2.7.5

### 🔨 Fixed

- Rounded to 2 decimal places

## 2.7.3

### 🔨 Fixed

- loading config.json
- check response length

## 2.7.0

### 🚀 Added

- heaters Consumption
- standalone container

## 2.6.3

### 🔨 Fixed

- own dict for ev stations

## 2.6.2

### 🔨 Fixed

- fixed issue with EVStation
- added missed readingTotal

## 2.6.0

### 🚀 Added

- EVStation
- EVStations with parameters

## 2.5.8

### 🔨 Fixed

- show live data if loglevel is DEBUG

## 2.5.7

### 👌 Improved

- bump viessmann-gridbox-connector to 2.5.1
- using viesmann-gridbox-connector module intern config.json
- adjust import

### 🔨 Fixed

- fixed gridboxconnector.sh script
- Settable Log Level

## 2.4.2

### 🔨 Fixed

- catch exception if no data is available

## 2.4.1

### 🚀 Added

- Image for Result

### 🔨 Fixed

- dockerfile source

## 2.3.0

### 🚀 Added

- added new sensor 'directConsumptionEV' to show the direct consumption of the EV

### 🔨 Fixed

- variable naming

## 2.1.2

### 🚀 Added

- Workflows to create releases
- scripts

## 2.0.0

### 🚀 Added

- using now s6-overlay
- Start with Unit Tests

## 1.11.0

### 🚀 Added

- Added S6-overlay

## 1.10.2

### 🚀 Added

- Added new sensor `directConsumptionHousehold` and `directConsumptionHeatPump` to show the direct consumption of the household
- Added new sensor `totalConsumption` to show the total consumption of the household
- Added Classes for the sensor to start with unit tests

### 🔨 Fixed

- Fixed the issue with the battery sum sensor
- Fixed the issue with the battery sum appliance id
- Fixed the issue with each battery show now correct values

## 1.9.12

### 🔨 Fixed

- Fixed Battery Sum set_state

## 1.9.11

### 🔨 Fixed

- Fixed Battery Sum ApplianceID

## 1.9.10

### 🔨 Fixed

- Revert to 1.5.0 maybe issue with Battery refactor code

## 1.9.9

### 🚀 Added

- Consumption Sensor
- Total Consumption Sensor

#### 🔨 Fixed

- Fixed version number
- Fixed copy script from dev to main
- Fixed config.yml

## 1.5.0

### 🚀 Added

- Consumption Sensor
- Total Consumption Sensor

#### 🔨 Fixed

- set Value only if available

## 1.4.5

#### 🔨 Fixed

- Code issue

## 1.4.4

### 🚀 Added

- mqtt settings

## 1.4.3

#### 🔨 Fixed

- Code issue

## 1.4.2

#### 🔨 Fixed

- Versionnumber

## 1.4.0

### 🚀 Added

- Sensor directConsumptionHousehold
- Sensor directConsumptionHeatPump
- Use py-lib connector

## 1.3.0

#### 🔨 Fixed

- wrong code (never use github online editor)

### 🚀 Added

- add Battery Power

## 1.2.0

#### 🔨 Fixed

- fixed casting battery stateOfCharge

### 🚀 Added

- battery capacity

## 1.1.3

#### 🔨 Fixed

- use correct battery information

## 1.1.2

- added Vendor

## 1.1.1

#### 🔨 Fixed

- use correct battery sensor_info

## 1.1.0

- Start with Battery support

## 1.0.10

- fixed python issue

## 1.0.9

- added one time print of data

## 1.0.8

- added dict check

## 1.0.7

- added delay if response is error

## 1.0.6

- fixed multiple generate id_token

## 1.0.5

- added more logs

## 1.0.4

- removed version string in code

## 1.0.3

- added version string

## 1.0.2

- added print to find out why not fetch id_token

## 1.0.1

- fixed refresh Auth Token
- Worked on the Documentation

## 1.0.0

- Initial release
- Added Mqtt Device Discovery
