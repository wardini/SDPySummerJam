# Written by Ben Abrams <abrams (dot) benjamin (at) gmail>
import pygame
import random
# import segments

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
        self.reset()
        self.color = "white"
        self.rect = pygame.Rect(self.x_pos-4, self.y_pos-4, 9, 9) # this rect might be the wrong size
        self.vector = pygame.math.Vector2(self.x_pos, self.y_pos)
        self.vec_dist = 100000
        self.twinkle_timer = 1500 + random.randint(0,5000)

    def reset(self):
        self.mouse_near = False
        self.selected = False
        self.connected = False
    
    def update(self, dt):
        if self.twinkle_timer < -35:
            self.twinkle_timer = 1500 + random.randint(0,1500)
        else:
            self.twinkle_timer -= dt
    
    def set_selected(self, value:bool):
        self.selected = value
    
    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.check_near(event.pos)
    
    def check_near(self, mouse_loc, dist_limit = 15.0):
        # Check if actual collision
        self.mouse_near = self.rect.collidepoint(mouse_loc)

        # check if current mouse position "near" current star loc
        if not self.mouse_near:
            mouse_vec = pygame.math.Vector2(mouse_loc)
            self.vec_dist = self.vector.distance_to(mouse_vec)

            if self.vec_dist <= dist_limit:
                # mouse within "close" distance limit
                self.mouse_near = True

    def draw(self, screen):
        if self.mouse_near:
            # mouse near state
            #pygame.draw.rect(screen, pygame.Color("yellow"),self.rect,4)
            pygame.draw.line(screen, pygame.Color("yellow"),(self.x_pos-4,self.y_pos),(self.x_pos+4,self.y_pos))
            pygame.draw.line(screen, pygame.Color("yellow"),(self.x_pos,self.y_pos-4),(self.x_pos,self.y_pos+4))
            pygame.draw.line(screen, pygame.Color("yellow"),(self.x_pos-2,self.y_pos-2),(self.x_pos+2,self.y_pos+2))
            pygame.draw.line(screen, pygame.Color("yellow"),(self.x_pos-2,self.y_pos+2),(self.x_pos+2,self.y_pos-2))

        if self.selected:
        # selected state
            #pygame.draw.rect(screen, pygame.Color("orange"),self.rect,2)

            # make a simple plus sign
            pygame.draw.line(screen, pygame.Color("orange"),(self.x_pos-4,self.y_pos),(self.x_pos+4,self.y_pos))
            pygame.draw.line(screen, pygame.Color("orange"),(self.x_pos,self.y_pos-4),(self.x_pos,self.y_pos+4))
            pygame.draw.line(screen, pygame.Color("orange"),(self.x_pos-2,self.y_pos-2),(self.x_pos+2,self.y_pos+2))
            pygame.draw.line(screen, pygame.Color("orange"),(self.x_pos-2,self.y_pos+2),(self.x_pos+2,self.y_pos-2))
        # connected state
        #else:
        # default state
        #    pygame.draw.rect(screen, pygame.Color(self.color),self.rect,2)

        # twinkle
        if self.twinkle_timer < 0:
            pygame.draw.rect(screen, pygame.Color("black"),self.rect,5)

    
    def get_pos(self):
        return((self.x_pos, self.y_pos))
    
    def get_state(self):
        return {
            "position": (self.x_pos, self.y_pos),
            "mouse_near": self.mouse_near,
            "selected": self.selected,
            "connected": self.connected,
            "color": self.color
        }
    
    def get_mouse_near(self,):
        return self.mouse_near

    def _validate_input(self, x_pos, y_pos):
        if not isinstance(x_pos, float) or not isinstance(y_pos, float):
            msg = f"Attempted to make a Star with positions of the wrong type! x_pos: {x_pos}, y_pos {y_pos}"
            print(msg)
            raise StarPositionError(msg, x_pos, y_pos)


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
