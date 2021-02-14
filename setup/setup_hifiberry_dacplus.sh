#!/bin/bash

# Setups the HifiBerry Dac+ to works with the Raspberry Pi
# Usage: sudo ./setup_hifiberry_dacplus.sh

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

if (( $EUID != 0 )) ; then
    echo "Execute this script with sudo permissions. Exiting..."
    exit
fi

sed -i -e "s/dtparam=audio=on/#&/g" /boot/config.txt
echo "Commented out 'dtparam=audio=on' in /boot/config.txt"

sed -i -e "/.*dtparam=audio.*/a dtoverlay=hifiberry-dacplus" /boot/config.txt
echo "Added 'dtoverlay=hifiberry-dacplus' in /boot/config.txt"

sed -i -e "/.*dtparam=audio.*/a force_eeprom_read=0" /boot/config.txt
echo "Added 'force_eeprom_read=0' in /boot/config.txt"

cp "$ROOT_DIR/setup/resources/asound.conf" "/etc/"
echo "Copied asound.conf to /etc/"
