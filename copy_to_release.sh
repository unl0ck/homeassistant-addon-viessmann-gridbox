#!/bin/bash

# Define source and target directories
src_dir="GridboxConnectorAddon-dev"
target_dir="GridboxConnectorAddon"

# Remove contents of target directory
rm -rf $target_dir/*
# Copy all files from source to target directory, overwriting existing files
cp -R $src_dir/* $target_dir/