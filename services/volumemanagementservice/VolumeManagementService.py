import configparser
import json
import time

from core.Service import Service
import struct
import socket

from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType

import alsaaudio


class VolumeManagementService(Service):

     def initialize(self):
        self.volume_percent_increment = self.config.getfloat('VolumePercentIncrement')
        self.volume_initial_percent = self.config.getfloat('VolumeInitialPercent')
        self.volume_percent = self.volume_initial_percent
        self.mixer = alsaaudio.Mixer('Master')
        self.core.dataRouter.subscribe(ModifierStateChangeNotification, self.handleModifierChange)
        self.set_volume(self.volume_percent)

    def handleModifierChange(self, modifier_change_notification):
        if modifier_change_notification.modifier_type == ModifierType.Increase:
            self.increaseVolume()
        elif modifier_change_notification.modifier_type == ModifierType.Decrease:
            self.decreaseVolume()

    def increaseVolume():
        self.set_volume(self.volume_percent + self.volume_percent_increment)

    def decreaseVolume():
        self.set_volume(self.volume_percent - self.volume_percent_increment)

    def set_volume(volume_percent):
        if volume_percent > 1.0:
            volume_percent = 1.0
        elif volume_percent < 0:
            volume_percent = 0
        else:
            self.volume_percent = volume_percent
        
        self.core.logger.log("Setting music volume to " + str(volume_percent))

        mixer.setvolume(volume_percent * 100)