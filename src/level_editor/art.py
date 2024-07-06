import os
import json
import pygame

class Art:
    def __init__(self,name,info):
        self.info = info

        filename = "graphics/"+name+".png"
        if not os.path.isfile(filename):
            print(f"Art image {filename} not found")
            self.input_graphic = pygame.Surface((100,100))
            self.input_graphic.fill(pygame.Color("white"))
        else:
            self.input_graphic = pygame.image.load(filename).convert_alpha()

        if "art_transforms" not in self.info.keys():
            self.info["art_transforms"] = {
                "scaling":1.0,
                "rotation":0.0,
                "trans_x":0,
                "trans_y":0,
                "alpha":255
            }
        self.apply_transforms(self.info["art_transforms"])

    def apply_transforms(self,t):
        self.graphic = pygame.transform.scale_by(self.input_graphic,t['scaling'])
        self.graphic = pygame.transform.rotate(self.graphic, t['rotation'])
        self.graphic.set_alpha(t["alpha"])

    def draw(self,window):
        x = self.info["art_transforms"]['trans_x']
        y = self.info["art_transforms"]['trans_y']
        window.blit(self.graphic,(x,y))
