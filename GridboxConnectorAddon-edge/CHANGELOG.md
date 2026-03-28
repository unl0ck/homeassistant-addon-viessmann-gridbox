## 3.1.11-edge
### 🔄 Changes
- fixed publish issue

## 3.1.10-edge
### 🔄 Changes
- update builder

## 3.1.9-edge
### 🔄 Changes
- fixed run tests
- added parallel run tests
- worked to automate create a build
- worked on workflow
- should fix workflow create release
- added bump version
- will create standalone only for stable tag
- updated requests
- updated workflow builder
- refactored code
- worked on logging
- update s6
- reworked on builder workflow
- worked on workflows
- update builder workflow

## 3.1.8-edge
### 🔄 Changes
- rework on release strategy
- refactor: migrate tests to pytest, add conftest.py, move to tests/
- using pytest
- fixed duplicate code
- build(deps): bump home-assistant/builder from 2026.02.1 to 2026.03.2
- build(deps): bump coverage
- build(deps): bump ha-mqtt-discoverable
- ci: bump edge 3.1.7 -> 3.1.8
- requirements.txt aktualisieren
- Remove redundant type variable, use key directly
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- Revert action version changes, keep only functional improvements
- Fix workflows and add stable versioning support
- Initial plan
- Use key variable instead of hardcoded strings for measurement.get()
- Add missing live and historical sensors, fix heatPump casing
- Use local timezone for historical statistics
- Add heatPumps MQTT sensor support
- Add state_class to live sensor models
- Fix invalid state_class metadata for historical sensors
- build(deps): bump logfire
- build(deps): bump ha-mqtt-discoverable
- build(deps): bump docker/setup-buildx-action from 3 to 4
- build(deps): bump docker/login-action from 3 to 4
- build(deps): bump docker/build-push-action from 6 to 7
- build(deps): bump opentelemetry-instrumentation-requests
- build(deps): bump logfire
- build(deps): bump home-assistant/builder from 2025.11.0 to 2026.02.1
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump logfire
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump logfire
- build(deps): bump bump-my-version
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump coverage
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump coverage
- build(deps): bump logfire
- build(deps): bump logfire
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump coverage
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump logfire
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector
- build(deps): bump bump-my-version
- build(deps): bump coverage
- another try to release Stable version
- removed daemon
- build(deps): bump ruff in /GridboxConnectorAddon-edge/GridboxConnector

<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 3.1.7
### 🔨 Fixed

- threading daemon removed
## 3.1.6-edge
### 🔨 Fixed

- threading

## 3.1.5-edge

### 🔨 Fixed

- eon-home endpoint set

## 3.1.4-edge

### 🔨 Fixed

- logfire log output corrected

## 3.1.3-edge

### 🚀 Added

- you can use an own logfire token to get logs
- you can set another loglevel as normal log, to reduce traffic on logfire

## 3.1.2-edge

### 🔨 Fixed

- using correct token

## 3.1.1-edge

### 🚀 Added

- New Logfire token

## 3.1.0-edge

### 🚀 Added

- Heatpump Sum added

## 3.0.12-edge

### 🔨 Fixed

- Historical power to energy fixed

### 🚀 Added

- tool to make it easier to get logs and screenshot of dashboard

## 3.0.11-edge

### 🔨 Fixed

- Heaters changed device_class and unit of measurement

## 3.0.10-edge

### 🔨 Fixed

- BatteryPower device_class to power changed

## 3.0.9-edge

### 🚀 Added

- heating in historical

## 3.0.7-edge

### 🚀 Added

- battery charge and discharge

## 3.0.6-edge

### 🚀 Added

- battery charge and discharge

## 3.0.3-edge

### 🚀 Added

- find file function

### 🚀 Added

- logs of file structure

## 3.0.2-edge

### 🚀 Added

- logs of content

## 3.0.0-edge

Is Currently not working correctly don't Use for Production
will released if all Sensors integrated like 2.x

### 🔄 Changed

- refactored the way of create sensors

## 2.11.66

### 🔄 Changed

- removed armhf and armv7 until it will working the build

## 2.11.65

### 🔨 Fixed

- using older builder imager

## 2.11.63

### 🔨 Fixed

- python runtime

## 2.11.62

### 🔨 Fixed

- build process adjusted

## 2.11.61

### 🔨 Fixed

- fixed grid in historical data
- fixed tests

## 2.11.60

### 🔨 Fixed

- fixed grid in historical data

## 2.11.59

### 🚀 Added

- test coverage report action

## 2.11.58

### 🔨 Fixed

- removed temp Battery value

## 2.11.57

### 🔨 Fixed

- added temp Battery value

## 2.11.56

### 🔨 Fixed

- added temp Battery value

## 2.11.55

### 🔨 Fixed

- version number

## 2.11.54

### 🔨 Fixed

- unit test for battery in historical data

## 2.11.53

### 🔨 Fixed

- fixed Historical Data Battery

## 2.11.52

### 🚀 Added

- setup.ini to read environment
- added unittest to workflow

## 2.11.51

### 🔨 Fixed

- fixed unittests
- fixed historical data exception workaround try catch
- modified unittests for batteries
- added logfire for logger only error logs

## 2.11.50

### 🔨 Fixed

- fixed battery live data sorry guys another try 🫠

## 2.11.49

### 🔨 Fixed

- fixed battery live data sorry guys

## 2.11.48

### 🔨 Fixed

- fixed build

## 2.11.47

### 🔨 Fixed

- fixed build

## 2.11.46

### 🔨 Fixed

- read telemetry option

## 2.11.43

### 🔨 Fixed

- removed logs from logfire

## 2.11.42

### 🔨 Fixed

- set correct environment

## 2.11.41

### 🔨 Fixed

- fixed telemetry default value

## 2.11.40

### 🔨 Fixed

- fixed more step by step good to be test it first on edge

## 2.11.39

### 🔨 Fixed

- last_reset should now working 🙈 🤷

### 🔄 Changed

- bump ha-mqtt-discoverable 0.16.4

## 2.11.35

### 🔨 Fixed

- logfire

### 🔄 Changed

- bump viessmann-gridbox-connector 1.6.0

## 2.11.33

### 🔨 Fixed

- logfire

### 🔄 Changed

- bump viessmann-gridbox-connector 1.7.0

## 2.11.31

### 🚀 Added

- make possible the disable and enable telemetry

### 🔨 Fixed

- sensitive filter fixed

## 2.11.28

### 🔨 Fixed

- sensitive filter fixed

## 2.11.26

### 🚀 Added

- start with logfire implementation

## 2.11.25

### 🔨 Fixed

- historical devices revert last_update

## 2.11.24

### 🔨 Fixed

- historical devices added last_update

### 🔄 Changed

- bump requests 2.32.3
- bump ha-mqtt-discoverable 0.16.3

## 2.11.23

### 🔨 Fixed

- historical devices added state_class

## 2.11.22

### 🔨 Fixed

- historical devices now energy not power devices

## 2.11.21

### 🔨 Fixed

- historical prefix

## 2.11.19

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
