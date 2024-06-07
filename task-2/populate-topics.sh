#!/bin/bash

echo "Starting generator..."
source kafka-venv/bin/activate

echo "Running generator..."
python3 generator.py "$@"

echo "Finished generator"
