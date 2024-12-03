#!/command/with-contenv bashio
# shellcheck shell=bash

echo "Starting Gridbox Connector Shell Script"
export MqttUser=$(bashio::config 'OverrideMqttUser')
export MqttPw=$(bashio::config 'OverrideMqttPw')
export MqttServer=$(bashio::config 'OverrideMqttServer')
export MqttPort=$(bashio::config 'OverrideMqttPort')
export TelemetryServer=$(bashio::config 'OverrideTelemetryUrl')

test "$MqttUser" = "null" && export MqttUser=$(bashio::services "mqtt" "username")
test "$MqttPw" = "null" && export MqttPw=$(bashio::services "mqtt" "password")
test "$MqttServer" = "null" && export MqttServer=$(bashio::services "mqtt" "host")
test "$MqttPort" = "null" && export MqttPort=$(bashio::services "mqtt" "port")
export USERNAME=$(bashio::config 'username')
export PASSWORD=$(bashio::config 'password')
export LOG_LEVEL=$(bashio::config 'log_level')
export ENABLE_TELEMETRY=$(bashio::config 'enable_telemetry')
export TELEMETRY_SERVER=$(bashio::config 'OverrideTelemetryUrl')
ls -lash /data
cd /build/
ls -lash
pwd
python GridboxConnector