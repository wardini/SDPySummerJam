import pygame
import random
import json

class Foreground:

    def __init__(self,glbls):
        self.glbls = glbls

        with open("graphics/foregrounds.json","r") as f:
            self.foregrounds = json.load(f)

    def new_level(self):

        selection = random.randrange(len(self.foregrounds))

        filename = "graphics/" + self.foregrounds[selection]
        self.forgpic = pygame.image.load(filename).convert_alpha()

    def draw(self,window):

        window.blit(self.forgpic,(0,self.glbls['HEIGHT'] - self.forgpic.get_rect()[3]))
