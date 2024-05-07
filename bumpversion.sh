#!/bin/bash

# Check if argument is provided
if [ -z "$1" ]
then
    echo "No argument supplied. Please provide 'major', 'minor', or 'patch'."
    exit 1
fi

# Run bump-my-version with the provided argument
bump-my-version bump $1 --config-file .bumpversion.toml