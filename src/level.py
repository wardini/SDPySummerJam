import json
import pygame
from txt_item import Txt_item
from star import Star
from segment import Segment
from band import Band

BAND_FIZZLE_TIME = 1 # seconds

def art_apply_transforms(input_graphic,t):
    graphic = pygame.transform.scale_by(input_graphic,t['scaling'])
    graphic = pygame.transform.rotate(graphic, t['rotation'])
    graphic.set_alpha(t["alpha"])
    return(graphic)


class Level:
    def __init__(self,const_name:str,glbls:dict):
        self.glbls = glbls
        self.name = const_name

        with open('constellations/'+const_name+'.json') as f:
            self.cinfo = json.load(f)

        self._load_background()

        self._load_objects()

        self.reset()

    def reset(self):
        self.found_segments = []
        self.current_band = None
        self.complete = False
        self.done = False
        self.time = 0
        self.state = "play"
        self.cur_alpha = 0
        self.delete_band = False
        self.anchor_star_idx = None
        self.dest_star_idx = None

    def process_event(self,event):

        for star in self.stars:
            star.process_event(event)
        if self.current_band:
            self.current_band.process_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # create new band if necessary
                if not self.current_band:
                    self.current_band = Band(event.pos)
                    self.delete_band = False
                # see if we clicked hear a star
                for idx in (range(0, len(self.stars) - 1)):
                    # because Segments are only aware of stars by their indices in
                    # the constellation JSON file, we must use those index values to create
                    # the preliminary segment
                    if self.stars[idx].get_mouse_near():
                        self.anchor_star_idx = idx
                if self.complete:
                    if self.t_done_button.check_select(event.pos):
                        self.done = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.current_band:                
                self.delete_band = True
                for idx in (range(0, len(self.stars) - 1)):
                    # because Segments are only aware of stars by their indices in
                    # the constellation JSON file, we must use those index values to create
                    # the preliminary segment
                    if self.stars[idx].get_mouse_near():
                        self.dest_star_idx = idx
        

    def update(self,dt):
        if self.state == "play":
            self.time += dt
            if self.time > 4000:
                self.state = "fade in"
                self.cur_alpha = 0

            for star in self.stars:
                star.update(dt)

            if self.current_band:
                self.current_band.update(dt)
            
            if self.delete_band and self.current_band and self.current_band.get_lifetime_exceeded():
                del self.current_band
                self.current_band = None

            # create new segment if necessary
            if self.dest_star_idx and self.anchor_star_idx:
                new_segment = Segment(self.anchor_star_idx, self.dest_star_idx)
                # see if segment is correct
                for segment in self.goal_segments:
                    if new_segment == segment:
                        self.found_segments.append(new_segment)
                        self.dest_star_idx = None
                        self.anchor_star_idx = None

            # check if game done
            if self.found_segments == self.goal_segments:
                self.complete = True
                self.state = "complete"

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
        self.t_level_name.render_text(window)

        for star in self.stars:
            star.draw(window)

        for segment in self.found_segments:
            segment.draw(window)

        if self.current_band:
            self.current_band.draw(window)
        
        if self.complete:
            self.t_done_button.render_text(window)
    
    def _load_background(self):
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
        self.t_level_name = Txt_item(self.name.title(),(0,0),False,None,fontsize=40)
        self.complete = False

        # finish button
        locx = self.glbls['WIDTH']-200
        locy = 50
        self.t_done_button = Txt_item("Next Level",(locx,locy),True,"Done",fontsize=40)

    def _load_objects(self):
        # create array of stars for level
        self.stars = []
        for star_coords in self.cinfo['stars']:
            new_star = Star(float(star_coords[0]), float(star_coords[1]))
            self.stars.append(new_star)

        # create list of goal segments
        self.goal_segments = []
        for segment in self.cinfo['segments']:
            new_segment = Segment(segment[0], segment[1])
            self.goal_segments.append(new_segment)

