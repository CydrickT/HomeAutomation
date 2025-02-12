import configparser
import json
import threading
import time
import os

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

        self.music_playing = False
        self.song_index = 0

        self.core.dataRouter.subscribe(GeneralStateChangeNotification, self.handleStateChange)
        os.putenv('DISPLAY', ':0.0')
        mixer.init()
        pygame.init()

    def handleStateChange(self, state_change_notification):
        if state_change_notification.general_state_type == GeneralStateType.SleepPreparation:
            self.play()
        else:
            self.stop()

    def play(self):
        self.music_playing = True
        mixer.music.set_volume(1.0)
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
