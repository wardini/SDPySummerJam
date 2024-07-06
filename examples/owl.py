import pygame
import random

''' 
   hooting owl
'''

class Owl:
    def __init__(self):
        self.time = 0

        self.hoot_sound = pygame.mixer.Sound("owl-hooting-48028.ogg")
        self.hoot_sound.set_volume(0.3)
  
        self.nexthoot = int(5000 + 20000 * random.random())

    def update(self,dt):

        self.time += dt

        if self.time > self.nexthoot:
            self.time = 0
            self.hoot_sound.play(0)
            self.nexthoot = int(15000 + 40000 * random.random())
            self.hoot_sound.set_volume(0.15)

            

