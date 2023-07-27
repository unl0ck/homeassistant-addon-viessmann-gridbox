#!/usr/bin/with-contenv bashio


export USERNAME=$(bashio::config 'username')
export PASSWORD=$(bashio::config 'password')
export MqttUser=$(bashio::services "mqtt" "username")
export MqttPw=$(bashio::services "mqtt" "password")
export MqttServer=$(bashio::services "mqtt" "host")
export MqttPort=$(bashio::services "mqtt" "port")
echo "Hello world!"
ls -lash /data
cat /data/options.json
cd /build/
ls -lash
pwd
python GridboxConnector