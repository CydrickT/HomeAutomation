import configparser
import json
import threading
import time

import pygame
import requests
from pygame import mixer

from core.Service import Service
from topics.generalstate.GeneralStateChangeNotification import GeneralStateChangeNotification
from topics.generalstate.GeneralStateType import GeneralStateType
from topics.modifierstate.ModifierStateChangeNotification import ModifierStateChangeNotification
from topics.modifierstate.ModifierType import ModifierType

MUSIC_END = pygame.USEREVENT+1

class MusicManagerService(Service):

    def initialize(self):
        self.music_playlist = json.loads(self.config['MusicPlaylist'])
        self.volume_percent_increment = self.config.getfloat('VolumePercentIncrement')
        self.volume_initial_percent = self.config.getfloat('VolumeInitialPercent')
        self.music_playing = False
        self.volume_percent = self.volume_initial_percent
        self.song_index = 0

        self.core.dataRouter.subscribe(GeneralStateChangeNotification, self.handleStateChange)
        self.core.dataRouter.subscribe(ModifierStateChangeNotification, self.handleModifierChange)
        mixer.init()
        pygame.init()
        print("Music Manager Service: Initialization Complete")

    def handleStateChange(self, state_change_notification):
        if state_change_notification.general_state_type == GeneralStateType.SleepPreparation:
            self.play()
        else:
            self.stop()

    def handleModifierChange(self, modifier_change_notification):
        if self.music_playing:
            if modifier_change_notification.modifier_type == ModifierType.Increase:
                self.increaseVolume()
            elif modifier_change_notification.modifier_type == ModifierType.Decrease:
                self.decreaseVolume()

    def play(self):
        self.music_playing = True
        self.set_volume(self.volume_initial_percent)
        self.start_song(self.music_playlist[self.song_index])

        monitoring_thread = threading.Thread(target=self.start_next_song_monitoring)
        monitoring_thread.start()

    def start_next_song_monitoring(self):
        mixer.music.set_endevent(MUSIC_END)
        pygame.event.clear()
        while self.music_playing:
            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    self.core.logger.log("Previous song ended. Starting new song.")
                    self.song_index += 1
                    nextSong = self.music_playlist[self.song_index % len(self.music_playlist)]
                    self.start_song(nextSong)
            time.sleep(0.1)
        self.core.logger.log("Stopping the next song thread")

    def start_song(self, song):
        self.core.logger.log("Playing song: " + song)
        mixer.music.load(song)
        mixer.music.play()

    def stop(self):
        self.core.logger.log("Stopping playing song.")
        self.music_playing = False
        self.song_index = 0
        mixer.music.stop()

    def increaseVolume(self):
        self.set_volume(self.volume_percent + self.volume_percent_increment)

    def decreaseVolume(self):
        self.set_volume(self.volume_percent - self.volume_percent_increment)

    def set_volume(self, volume_percent):
        if volume_percent > 1.0:
            volume_percent = 1.0
        elif volume_percent < 0:
            volume_percent = 0
        else:
            self.volume_percent = volume_percent

        self.core.logger.log("Setting music volume to " + str(volume_percent))
        mixer.music.set_volume(volume_percent)
