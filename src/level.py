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

        self.click_sound = pygame.mixer.Sound("audio/click.ogg")
        self.click_sound.set_volume(1)

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
                    self.current_band = Band(event.pos, self.glbls)
                    self.delete_band = False
                # see if we clicked hear a star
                for idx in (range(0, len(self.stars))):
                    # because Segments are only aware of stars by their indices in
                    # the constellation JSON file, we must use those index values to create
                    # the preliminary segment
                    if self.stars[idx].get_mouse_near():
                        self.anchor_star_idx = idx
                        self.stars[self.anchor_star_idx].set_selected(True)
                        break
                if self.complete:
                    if self.t_done_button.check_select(event.pos):
                        self.done = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.current_band:                
                # self.delete_band = True
                for idx in (range(0, len(self.stars))):
                    # because Segments are only aware of stars by their indices in
                    # the constellation JSON file, we must use those index values to create
                    # the preliminary segment
                    self.stars[idx].set_selected(False)
                    if self.stars[idx].get_mouse_near():
                        self.dest_star_idx = idx
                        break
                del self.current_band
                self.current_band = None
        

    def update(self,dt):
        if self.state == "play":
            self.time += dt

            for star in self.stars:
                star.update(dt)

            if self.current_band:
                self.current_band.update(dt)

            for segment in self.goal_segments:
                segment.update(dt)

            # create new segment if necessary
            if self.dest_star_idx is not None and self.anchor_star_idx is not None and self.dest_star_idx != self.anchor_star_idx:
                new_segment = Segment(self.anchor_star_idx, self.dest_star_idx)
                for segment in self.goal_segments:
                    if new_segment == segment:
                        new_segment.set_position(self.stars)
                        self.found_segments.append(new_segment)
                        self.stars[self.anchor_star_idx].set_selected(False)
                        self.click_sound.play()
                        break
                self.dest_star_idx = None
                self.anchor_star_idx = None

            # check if game done
            if len(self.found_segments) == len(self.goal_segments):
                self.state = "fade in"

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

        for segment in self.goal_segments:
            segment.draw(window, draw_type="goal")

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
        self.iconimage = pygame.transform.rotate(self.iconimage,self.cinfo['art_transforms']['rotation'])
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
            new_segment.set_position(self.stars)
            self.goal_segments.append(new_segment)

