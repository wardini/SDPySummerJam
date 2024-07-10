import pygame
import random
import json

class Insects:

    def __init__(self):

        with open("audio/insects.json","r") as f:
            self.isounds = json.load(f)

        self.playing_sound = False

    def new_level(self):

        if self.playing_sound:
            self.cricket_sound.stop()
            self.playing_sound = False

        selection = random.randrange(len(self.isounds))

        filename = "audio/" + self.isounds[selection][0]
        volume = self.isounds[selection][1]

        self.cricket_sound = pygame.mixer.Sound(filename)
        self.cricket_sound.set_volume(volume)
        self.cricket_sound.play(-1)

        self.playing_sound = True
