# Written by Ben Abrams <abrams (dot) benjamin (at) gmail>
import pygame
#import segments

"""
Methods
    init (x,y)
    reset()
        clear all states
    update(dt)
        if in twinkle mode, update twinkle
    check_near(mouse x, mouse y)
        if mouse near star
            set mouse_near_flag
    draw(screen)
        if twinkle
            draw twinkle graphics
        if mouse_near_flag
            draw mouse near effects

"""

class Star:
    def __init__(self, x_pos:float, y_pos:float) -> None:
        
        self._validate_input(x_pos, y_pos)
        # set position
        self.x_pos = x_pos
        self.y_pos = y_pos

        # initialize states
        self.mouse_near = False
        self.selected = False
        self.connected = False
        self.neighbors = []
        self.connected_segments = []
        self.color = "white"
        self.rect = pygame.Rect(self.x_pos-4, self.y_pos-4, 9, 9)

    def reset(self):
        self.mouse_near = False
        self.selected = False
        self.connected = False
        self.neighbors = []
        self.connected_segments = []
    
    def update(self, dt):
        pass
    
    def check_near(self, mouse_loc, dist_limit = 5):
        # Check if actual collision
        self.mouse_near = self.rect.collidepoint(mouse_loc)

        # check if current mouse position "near" current star loc
        if not self.mouse_near:
            if (abs(mouse_loc[0] - self.x_pos) <= dist_limit) or (abs(mouse_loc[1] - self.y_pos) <= dist_limit):
                # mouse within "close" distance limit
                self.mouse_near = True
    
    #def add_neighbor(self, new_neighbor: Star):
    #    self.neighbors.append(new_neighbor)

    def add_segment(self, new_segment):
        self.connected_segments.append(new_segment)

    def draw(self, screen):
        if self.mouse_near:
            # mouse near state
            pygame.draw.rect(screen, pygame.Color("orange"),self.rect,4)
        # selected state
        # connected state
        else:
        # default state
            pygame.draw.rect(screen, pygame.Color("yellow"),self.rect,2)
        pass
    
    def get_pos(self):
        return((self.x_pos, self.y_pos))
    
    def get_state(self):
        return {
            "position": (self.x_pos, self.y_pos),
            "mouse_near": self.mouse_near,
            "selected": self.selected,
            "connected": self.connected,
            "neighbors": self.neighbors,
            "connected_segments": self.connected_segments
        }
    
    def get_mouse_near(self,):
        return self.mouse_near

    def _validate_input(self, x_pos, y_pos):
        if not isinstance(x_pos, float) or not isinstance(y_pos, float):
            msg = f"Attempted to make a Star with positions of the wrong type! x_pos: {x_pos}, y_pos {y_pos}"
            print(msg)
            raise StarPositionError(msg, x_pos, y_pos)
        #TODO check for x, y positions out of range based on game's screen resolution


class StarPositionError(Exception):
    """
    Raised when a star is created with bad position variables

    Args:
        msg (str): detailed description of the error
        x_pos (): the entered x_position value
        y_pos (): the entered y_position value
    """
    def __init__(self, msg: str, x_pos, y_pos):
        self.msg = msg
        self.x_pos = x_pos
        self.y_pos = y_pos
        super().__init__
