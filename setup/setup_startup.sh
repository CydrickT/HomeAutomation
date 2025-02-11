#!/bin/bash
# Installation script for Home Automation
# Sets up a Systemd start script for the Home Automation python program
# Usage: sudo ./install_startup.sh

CONFIGURATION_FILE_NAME="HomeAutomation.config"
SYSTEMD_FILES_DESTINATION_PATH="/etc/systemd/system"

if (( $EUID != 0 )) ; then
    echo "Execute this script with sudo permissions. Exiting..."
    exit
fi

echo "Installing libffi-dev"
sudo apt install -y libffi-dev
echo "Installed libffi-dev"

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
PYTHON_LOC="$(which python3)"

APP_DIR="$ROOT_DIR"
echo "Enter the path of the application directory [$APP_DIR]:"
read INPUT_APP_DIR
if [ "$INPUT_APP_DIR" != "" ] ; then
    APP_DIR=$INPUT_APP_DIR
fi
echo "Selected application directory: $APP_DIR"

CONFIG_FILE="$APP_DIR/$CONFIGURATION_FILE_NAME"
echo "Enter the path of the configuration file [$CONFIG_FILE]"
read INPUT_CONFIG_FILE
if [ "$INPUT_CONFIG_FILE" != "" ] ; then
    CONFIG_FILE=$INPUT_CONFIG_FILE
fi
echo "Selected configuration file: $CONFIG_FILE"

rm -rf "$SYSTEMD_FILES_DESTINATION_PATH/homeautomation.service"
cp "$ROOT_DIR/setup/resources/homeautomation.service" "$SYSTEMD_FILES_DESTINATION_PATH"
sed -i -e "s#PYTHON_LOC#$PYTHON_LOC#g" "$SYSTEMD_FILES_DESTINATION_PATH/homeautomation.service"
sed -i -e "s#APP_DIR#$APP_DIR#g" "$SYSTEMD_FILES_DESTINATION_PATH/homeautomation.service"
sed -i -e "s#CONFIG_FILE#$CONFIG_FILE#g" "$SYSTEMD_FILES_DESTINATION_PATH/homeautomation.service"
echo "Copied file to $SYSTEMD_FILES_DESTINATION_PATH/homeautomation.service"

systemctl daemon-reload
systemctl enable homeautomation.service

echo "Setup homeautomation.service to start upon system startup."
