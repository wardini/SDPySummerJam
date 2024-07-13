# Written by Ben Abrams <abrams (dot) benjamin (at) gmail>
import pygame
# import segments


class Band:
    def __init__(self, position:tuple, glbls:dict) -> None:
        
        # set position
        self.start_x = position[0]
        self.start_y = position[1]
        self.glbls = glbls

        # initialize states
        self.reset()
        self.color = "white"
        # self.rect = pygame.Rect(self.x_pos, self.y_pos, 1, 1) # this rect might be the wrong size
        self.vector = pygame.math.Vector2(self.start_x, self.start_y)
        self.vec_dist = 100000

    def reset(self):
        self.lifetime_exceeded = False
        self.end_x = None
        self.end_y = None
        self.lifetime_count_enable = False
        self.lifetime_count = None

    def update(self, dt):
        if self.lifetime_count_enable:
            self.lifetime_count += dt
        
            if self.lifetime_count >= self.glbls.get('band_lifetime'):
                self.lifetime_exceeded = True

    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION and not self.lifetime_count_enable:
            (end_x, end_y) = event.pos
            self.end_x = end_x
            self.end_y = end_y
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.lifetime_count_enable = True
            self.lifetime_count = 0
            self.end_x = None
            self.end_y = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.lifetime_count_enable = False
            self.lifetime_count = None
            self.lifetime_exceeded = False


    def draw(self, screen):
        if self.end_x and self.end_y:
            points = (self.start_x,self.start_y),(self.end_x,self.end_y)
            pygame.draw.line(screen, pygame.Color("orange"),*points,width=2)

    def get_lifetime_exceeded(self):
        return self.lifetime_exceeded
    