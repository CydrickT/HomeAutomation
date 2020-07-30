#!/bin/bash

apt-get update
apt-get dist-upgrade
apt-get install alsa-utils
sync
modprobe snd_bcm2835
amixer cset numid=3 1