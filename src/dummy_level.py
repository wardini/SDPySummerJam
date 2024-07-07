import json
import pygame
from txt_item import Txt_item

# this is a dummy level class
# so I can work on and complete
# the gameplay screen

def art_apply_transforms(input_graphic,t):
    graphic = pygame.transform.scale_by(input_graphic,t['scaling'])
    graphic = pygame.transform.rotate(graphic, t['rotation'])
    graphic.set_alpha(t["alpha"])
    return(graphic)

class Level:
    def __init__(self,const_name,glbls):
        self.glbls = glbls

        with open('constellations/'+const_name+'.json') as f:
            self.cinfo = json.load(f)

        # get start image
        self.graphic = pygame.image.load("constellations/"+self.cinfo['starmap']).convert()

        # get art image   -- note that blitting with alpha is very slow --
        orig_artimage = pygame.image.load("graphics/"+self.cinfo['artimage']).convert_alpha()
        self.artimage = art_apply_transforms(orig_artimage,self.cinfo['art_transforms'])
        self.artimage.set_alpha(0)

        # get icon image (hint image ??)
        w = orig_artimage.get_width()
        h = orig_artimage.get_height()
        iconscale = 300 / (w**2+h**2)**0.5
        self.iconimage = pygame.transform.scale_by(orig_artimage,iconscale)
        self.iconlocation = (10, 50)
        
        # Create label for the level
        self.name = Txt_item(const_name.title(),(0,0),False,None,fontsize=40)
        self.complete = False

        # finish button
        locx = self.glbls['WIDTH']-200
        locy = self.glbls['HEIGHT']-50
        self.done_button = Txt_item("Next Level",(locx,locy),True,"Done",fontsize=40)

        self.reset()

    def reset(self):
        self.complete = False
        self.done = False
        self.time = 0
        self.state = "play"
        self.cur_alpha = 0

    def process_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.complete:
                    if self.done_button.check_select(event.pos):
                        self.done = True

    def update(self,dt):
        if self.state == "play":
            self.time += dt
            if self.time > 4000:
                self.state = "fade in"
                self.cur_alpha = 0
        elif self.state == "fade in":
            self.cur_alpha += 1
            self.artimage.set_alpha(self.cur_alpha)
            if self.cur_alpha > self.cinfo['art_transforms']['alpha']:
                self.complete = True
                self.state = "complete"


    def draw(self,window):
        #window.fill(pygame.Color("black"))
        window.blit(self.graphic,(0,0))

        if self.state == "fade in" or self.state == "complete":
            x = self.cinfo['art_transforms']['trans_x']
            y = self.cinfo['art_transforms']['trans_y']
            window.blit(self.artimage,(x,y))

        window.blit(self.iconimage,self.iconlocation)
        self.name.render_text(window)

        if self.complete:
            self.done_button.render_text(window)
