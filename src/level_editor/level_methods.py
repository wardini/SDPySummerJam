import os
import json
import pygame

def load_level(const_name,glbls):

    if not os.path.isfile("constellations/"+const_name+".png"):
        print("Constellation image not found")
        graphic = pygame.Surface((glbls["WIDTH"],glbls["HEIGHT"]))
        graphic.fill(pygame.Color("black"))
    else:
        graphic = pygame.image.load("constellations/"+const_name+".png").convert_alpha()

    if not os.path.isfile("constellations/solution_"+const_name+".png"):
        print("Constellation solution image not found")
        solution_graphic = pygame.Surface((glbls["WIDTH"],glbls["HEIGHT"]))
        solution_graphic.fill(pygame.Color("black"))
    else:
        solution_graphic = pygame.image.load("constellations/solution_"+const_name+".png").convert_alpha()

    if not os.path.isfile("constellations/"+const_name+".json"):
        info = {"stars":[],"segments":[]}
    else:
        with open("constellations/"+const_name+".json","r") as f:
            info = json.load(f)

    return graphic,solution_graphic,info

def save_level(const_name,info):
    save_text = json.dumps(info,indent=4)
    with open("constellations/"+const_name+".json","w") as f:
        f.write(save_text)
