import pygame
from txt_item import Txt_item
#from level import Level
from dummy_level import Level
import json
from insects import Insects
from owl import Owl
from firefly import FireFly
from foreground import Foreground
from shootingstar import ShootingStar

class Gameplay:
    def __init__(self,glbls):
        self.glbls = glbls
        self.done = False
        self.quit = False
        self.next_state = None  # this game has only this screen

        # all the defined levels including intro and congrats levels
        with open("constellations/constellations.json","r") as f:
            self.const_names = json.load(f)

        # load levels
        self.levels = []
        for c in self.const_names:
            self.levels.append(Level(c,self.glbls))
        self.cur_level = 0

        # debug frame rate display when 'f' key pressed
        self.glbls['ti_fps'] = Txt_item('00',(self.glbls['WIDTH']-50,0),False,None)
        self.show_fps = False

        # insect sounds
        self.insects = Insects()
        # owl sounds
        self.owl = Owl()

        # firefly graphics
        self.Nffs = 100
        self.ffs = []
        for i in range(self.Nffs):
            self.ffs.append(FireFly(10,self.glbls['HEIGHT']-50,self.glbls['WIDTH']-10,self.glbls['HEIGHT']-10))

        # foregrounds
        self.foreground = Foreground(self.glbls)

        # shooting stars
        self.ss1 = ShootingStar(200,self.glbls['WIDTH']-200,200,self.glbls['HEIGHT']-200)
        self.ss2 = ShootingStar(200,self.glbls['WIDTH']-200,200,self.glbls['HEIGHT']-200)

    def startup(self):
        self.new_level()

    def new_level(self):
        self.play_state = "game"
        self.insects.new_level()
        self.foreground.new_level()

    def update(self,dt):
        self.levels[self.cur_level].update(dt)

        # check if we should advance to next level or quit
        if self.levels[self.cur_level].done:
            self.cur_level += 1
            if self.cur_level == len(self.levels):
                self.done = True
                self.quit = True
                self.cur_level = len(self.levels)-1
            else:
                self.new_level()
            self.levels[self.cur_level].reset()

        # update the environment items
        self.owl.update(dt)
        self.ss1.update(dt)
        self.ss2.update(dt)
        for f in self.ffs:
            f.update(dt)

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
        #window.fill(pygame.Color("black"))   # full star screen overwites this anyway

        self.levels[self.cur_level].draw(window)

        if self.show_fps:
            self.glbls['ti_fps'].change_text(str(self.glbls['frame_rate']))
            self.glbls['ti_fps'].render_text(window)

        # display environment items
        self.foreground.draw(window)

        for f in self.ffs:
            f.draw(window)

        self.ss1.draw(window)
        self.ss2.draw(window)
