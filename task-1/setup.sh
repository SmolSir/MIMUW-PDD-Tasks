#!/bin/bash

URL="https://drive.google.com/file/d/1lv4aDS8LrR8LnlKhtaf-bBOnjmaPIHjg/view?usp=drive_link"
ZIP_NAME="data.zip"
DATA_DIR="data"

# download the data zip
wget "$URL" -O "$ZIP_NAME"

# unzip
unzip "$ZIP_NAME" -d "$DATA_DIR"

# remove the zip
rm "$ZIP_NAME"
