#!/bin/bash
# Installation script for setupping a Raspberry Pi as a Bluetooth Speaker
# Is based on Frederic Danis script here: https://www.collabora.com/news-and-blog/blog/2022/09/02/using-a-raspberry-pi-as-a-bluetooth-speaker-with-pipewire-wireplumber/
# Usage: sudo ./install_bluetooth_speaker.sh

SYSTEMD_FILES_DESTINATION_PATH="/etc/systemd/system"

if (( $EUID != 0 )) ; then
    echo "Execute this script with sudo permissions. Exiting..."
    exit
fi

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

APP_DIR="$ROOT_DIR"
echo "Enter the path of the application directory [$APP_DIR]:"
read INPUT_APP_DIR
if [ "$INPUT_APP_DIR" != "" ] ; then
    APP_DIR=$INPUT_APP_DIR
fi
echo "Selected application directory: $APP_DIR"

echo "Installing python3-dbus"
sudo apt install -y python3-dbus
echo "Installed python3-dbus"

echo "Setting BlueZ daemon to allow re-pairing"
sed -i 's/#JustWorksRepairing.*/JustWorksRepairing = always/' /etc/bluetooth/main.conf
echo "Done setting up BlueZ for auto-repairing"

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
PYTHON_DBUS_LOC="$(which python)"

echo "Copying systemd file"

rm -rf "$SYSTEMD_FILES_DESTINATION_PATH/speaker-agent.service"
cp "$ROOT_DIR/setup/resources/speaker-agent.service" "$SYSTEMD_FILES_DESTINATION_PATH"
sed -i -e "s#PYTHON_DBUS_LOC#$PYTHON_DBUS_LOC#g" "$SYSTEMD_FILES_DESTINATION_PATH/speaker-agent.service"
sed -i -e "s#APP_DIR#$APP_DIR/setup/resources#g" "$SYSTEMD_FILES_DESTINATION_PATH/speaker-agent.service"
echo "Copied file to $SYSTEMD_FILES_DESTINATION_PATH/speaker-agent.service"

systemctl daemon-reload
systemctl enable speaker-agent.service

echo "Setup speaker-agent.service to start upon system startup."
