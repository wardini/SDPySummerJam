import pygame
import random

''' 
   cricketing owl
'''

class Crickets:
    def __init__(self):
        self.cricket_sound = pygame.mixer.Sound("insekt001.ogg")
        self.cricket_sound.set_volume(0.2)
        self.cricket_sound.play(-1)

