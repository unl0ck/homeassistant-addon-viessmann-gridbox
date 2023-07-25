#!/usr/bin/with-contenv bashio


export USERNAME=$(bashio::config 'username')
export PASSWORD=$(bashio::config 'password')
echo "Hello world!"
ls -lash /data
cat /data/options.json
cd /build/
ls -lash
pwd
python GridboxConnector