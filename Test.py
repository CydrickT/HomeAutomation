import configparser
import json
import sys
import threading
import time

import pygame
import requests
from pygame import mixer

MUSIC_END = pygame.USEREVENT+1

class TestMusicManagerService():

    def __init__(self):
        print(">>>" + sys.argv[1] + "<<<")
        self.music_playlist = json.loads(sys.argv[1])
        self.volume_percent_increment = 0.1
        self.volume_initial_percent = 1.0
        self.music_playing = False
        self.volume_percent = self.volume_initial_percent
        self.song_index = 0

        mixer.init()
        print("PYGAME INIT")
        pygame.init()
        time.sleep(2)
        self.play()

        while True:
            pass

    def play(self):
        self.music_playing = True
        self.set_volume(self.volume_initial_percent)
        self.start_song(self.music_playlist[self.song_index])

        self.start_next_song_monitoring()
        #monitoring_thread = threading.Thread(target=self.start_next_song_monitoring)
        #monitoring_thread.start()

    def start_next_song_monitoring(self):
        mixer.music.set_endevent(MUSIC_END)
        pygame.event.clear()
        while self.music_playing:
            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    print("Previous song ended. Starting new song.")
                    self.song_index += 1
                    nextSong = self.music_playlist[self.song_index % len(self.music_playlist)]
                    self.start_song(nextSong)
            time.sleep(0.1)
        print("Stopping the next song thread")

    def start_song(self, song):
        print("Playing song: " + song)
        mixer.music.load(song)
        mixer.music.play()

    def stop(self):
        print("Stopping playing song.")
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

        print("Setting music volume to " + str(volume_percent))
        mixer.music.set_volume(volume_percent)

TestMusicManagerService()