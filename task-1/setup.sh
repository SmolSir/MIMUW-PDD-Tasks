#!/bin/bash

ZIP_ID="1lv4aDS8LrR8LnlKhtaf-bBOnjmaPIHjg"
ZIP_NAME="data.zip"
DATA_DIR="data"

# download the data zip
gdown "$ZIP_ID" -O "$ZIP_NAME"

# unzip
unzip "$ZIP_NAME" -d "$DATA_DIR"

# remove the zip
rm "$ZIP_NAME"
