# Written by Ben Abrams <abrams (dot) benjamin (at) gmail>
import pygame
# import segments


class Band:
    def __init__(self, position:tuple) -> None:
        
        # set position
        self.x_pos = position[0]
        self.y_pos = position[1]

        # initialize states
        self.reset()
        self.color = "white"
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 1, 1) # this rect might be the wrong size
        self.vector = pygame.math.Vector2(self.x_pos, self.y_pos)
        self.vec_dist = 100000

    def reset(self):
        self.lifetime_exceeded = False

    def update(self, dt):
        pass

    def process_event(self, event):
        pass

    def draw(self, screen):
        pass

    def check_progress(self,):
        pass
    
    def get_lifetime_exceeded(self):
        return self.lifetime_exceeded
    