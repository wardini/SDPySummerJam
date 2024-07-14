import pygame
import random
import json

class Insects:

    def __init__(self):

        self.cricket_sound = pygame.mixer.Sound("audio/insect1.ogg")
        self.cricket_sound.set_volume(0.2)
        self.cricket_sound.play(-1)

    def new_level(self):
        pass
