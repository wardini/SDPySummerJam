import pygame
from txt_item import Txt_item
#from level import Level
from dummy_level import Level
import json

class Gameplay:
    def __init__(self,glbls):
        self.glbls = glbls
        self.done = False
        self.quit = False
        self.next_state = None

        with open("constellations/constellations.json","r") as f:
            self.const_names = json.load(f)

        # load levels
        self.levels = []
        for c in self.const_names:
            self.levels.append(Level(c,self.glbls))
        self.cur_level = 0

        self.glbls['ti_fps'] = Txt_item('00',(self.glbls['WIDTH']-50,0),False,None)
        self.show_fps = False

        self.play_state = "game"

        self.levels[self.cur_level] = Level('andromeda',self.glbls)

    def startup(self):
        self.play_state = "game"

    def update(self,dt):
        self.levels[self.cur_level].update(dt)

        if self.levels[self.cur_level].done:
            self.cur_level += 1
            if self.cur_level == len(self.levels):
                self.done = True
                self.quit = True
                self.cur_level = len(self.levels)-1
            self.levels[self.cur_level].reset()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_q:
                self.done = True
                self.quit = True
            elif event.key == pygame.K_f:
                self.show_fps = not self.show_fps
        else:
            self.levels[self.cur_level].process_event(event)

    def draw(self, window):
        #window.fill(pygame.Color("black"))

        self.levels[self.cur_level].draw(window)

        if self.show_fps:
            self.glbls['ti_fps'].change_text(str(self.glbls['frame_rate']))
            self.glbls['ti_fps'].render_text(window)

