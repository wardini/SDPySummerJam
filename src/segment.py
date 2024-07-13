# Written by Ben Abrams <abrams (dot) benjamin (at) gmail>
import pygame
# import segments


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

    def __eq__(self, other):
        if isinstance(other, Segment):
            return((self.anchor_1 in other.anchors) and (self.anchor_2 in other.anchors))
        return NotImplemented


    def reset(self):
        pass
    
    def update(self, dt):
        pass

    def draw(self, screen):
        pass