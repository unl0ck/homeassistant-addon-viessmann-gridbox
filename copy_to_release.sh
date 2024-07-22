#!/bin/bash

# Define source and target directories
src_dir="GridboxConnectorAddon-dev"
target_dir="GridboxConnectorAddon"

# Copy all files from source to target directory, excluding config.yml and build.yml
rsync -av --delete --exclude='config.yaml' --exclude='build.yaml' --exclude='__pycache__' --exclude='.pytest_cache' $src_dir/ $target_dir/

yaml_datei="GridboxConnectorAddon/config.yaml"
current_version=$(yq -e '.version' $yaml_datei)
echo "Current version: $current_version"
new_version=$(jq -r '.version' GridboxConnectorAddon/rootfs/share/cloudSettings.json)
echo "New version: $new_version"

# Update the version in the config.yaml file

sed -i "s/version: \"$current_version\"/version: \"$new_version\"/g" $yaml_datei
#sed -i "" "s/version: \"$current_version\"/version: \"$new_version\"/g" $yaml_datei
