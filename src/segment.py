# Written by Ben Abrams <abrams (dot) benjamin (at) gmail>
import pygame
# import segments
from star import Star
import random


class Segment:
    def __init__(self, anchor_1:int, anchor_2:int) -> None:

        if anchor_1 == anchor_2:
            # cannot have the two anchor ports be the same
            raise Exception
        
        # set position
        self.anchor_1= anchor_1
        self.anchor_2 = anchor_2
        self.anchors = [anchor_1, anchor_2]

        # initialize states
        self.reset()
        self.color = "white"
        # self.rect = pygame.Rect(self.x_pos-4, self.y_pos-4, 9, 9) # this rect might be the wrong size
        # self.vector = pygame.math.Vector2(self.x_pos, self.y_pos)
        # self.vec_dist = 100000

        self.hint_timer = 2500 + random.randint(0,2000)

    def __eq__(self, other):
        if isinstance(other, Segment):
            return((self.anchor_1 in other.anchors) and (self.anchor_2 in other.anchors))
        return NotImplemented

    def set_position(self, stars):
        # extract the coordinates of the anchor stars given the array of stars
        self.anchor_1_pos = stars[self.anchor_1].get_pos()
        self.anchor_2_pos = stars[self.anchor_2].get_pos()

    def reset(self):
        self.anchor_1_pos = None
        self.anchor_2_pos = None

    
    def update(self, dt):
        if self.hint_timer < -300:
            self.hint_timer = 1500 + random.randint(0,1500)
        else:
            self.hint_timer -= dt

    def draw(self, screen, draw_type="found"):
        if self.anchor_1_pos and self.anchor_2_pos and draw_type == "found":
            points = self.anchor_1_pos, self.anchor_2_pos
            pygame.draw.line(screen, pygame.Color(self.color),*points,width=2)

        if self.hint_timer < 0 and draw_type == "goal":
           points = self.anchor_1_pos, self.anchor_2_pos
           pygame.draw.line(screen, pygame.Color("gray15"),*points,width=2)
