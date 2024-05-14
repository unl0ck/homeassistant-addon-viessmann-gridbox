#!/bin/bash

# Define source and target directories
src_dir="GridboxConnectorAddon-dev"
target_dir="GridboxConnectorAddon"

# Copy all files from source to target directory, excluding config.yml and build.yml
rsync -av --exclude='config.yaml' --exclude='build.yaml' --exclude='__pycache__' --exclude='.pytest_cache' $src_dir/ $target_dir/
# Read the current version from .bumpversion-dev.toml
current_version=$(jq -r '.version' GridboxConnectorAddon/rootfs/share/cloudSettings.json)

# Update the version in the config.yaml file
sed -i '' "s/version: \".*\"/version: \"$current_version\"/" GridboxConnectorAddon/config.yaml

