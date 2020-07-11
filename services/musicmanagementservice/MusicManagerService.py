import configparser
import json

import pygame
import requests
from pygame import mixer

from core.Service import Service
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType
from topics.modifierstate.ModifierStateChangeNotification import ModifierStateChangeNotification
from topics.modifierstate.ModifierType import ModifierType

SONG_END = 2514
class MusicManagerService(Service):

    def __init__(self, core):
        self.core = core
        config = configparser.ConfigParser()
        config.read('C:\\Users\\cydtr\\PycharmProjects\\HomeAutomation\\services\\musicmanagementservice\\MusicManagerService.config')
        self.music_playlist = json.loads(config['ServiceSpecific']['MusicPlaylist'])
        self.volume_percent_increment = int(config['ServiceSpecific']['VolumePercentIncrement'])
        self.volume_initial_percent = int(config['ServiceSpecific']['VolumeInitialPercent'])
        self.music_playing = False
        self.percent_volume = self.volume_initial_percent
        self.song_index = 0

    def initialize(self):
        self.core.dataRouter.subscribe(GeneralStateChangeNotification(), self.handleStateChange)
        self.core.dataRouter.subscribe(ModifierStateChangeNotification(), self.handleModifierChange)
        pygame.init()
        mixer.init()

    def handleStateChange(self, state_change_notification):
        if state_change_notification.general_state_type == GeneralStateType.SleepPreparation:
            self.play()
        elif state_change_notification.general_state_type == GeneralStateType.TrueSleep:
            self.stop()

    def handleModifierChange(self, modifier_change_notification):
        if self.music_playing:
            if modifier_change_notification.modifier_type == ModifierType.Increase:
                self.increaseVolume()
            elif modifier_change_notification.modifier_type == ModifierType.Decrease:
                self.decreaseVolume()

    def play(self):
        self.music_playing = True
        mixer.music.set_endevent(SONG_END)
        self.start_song(self.music_playlist[self.song_index])
        while self.music_playing:
           for event in pygame.event.get(SONG_END):
               self.start_song(self.music_playlist[self.song_index])

    def start_song(self, song):
        mixer.music.load(song)
        self.set_volume(self.percent_volume)
        mixer.music.play()

    def stop(self):
        self.music_playing = False
        mixer.music.stop()

    def increaseVolume(self):
        self.set_volume(self.percent_volume + self.volume_percent_increment)

    def decreaseVolume(self):
        self.set_volume(self.percent_volume - self.volume_percent_increment)

    def set_volume(self, volume_percent):
        self.core.logger.log("Setting music volume to " + str(volume_percent))
        self.percent_volume = volume_percent
        mixer.music.set_volume(volume_percent)
