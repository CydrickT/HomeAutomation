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
        self.music_playing = False
        self.song_index = 0

        mixer.init()
        print("PYGAME INIT")
        pygame.init()
        time.sleep(2)

        while True:
            pass

    def play(self):
        self.music_playing = True
        mixer.music.set_volume(1.0)
        self.start_song(self.music_playlist[self.song_index])
        self.start_next_song_monitoring()

    def start_next_song_monitoring(self):
        mixer.music.set_endevent(MUSIC_END)
        while mixer.get_busy() is None:
            print("busy")

        pygame.event.clear()

        while self.music_playing:
            if mixer.get_busy() is not None:
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


t = TestMusicManagerService()
t.play()