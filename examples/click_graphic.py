import pygame
import random

class Click_Graphic:
    def __init__(self,x,y):
        self.x,self.y = x,y
        self.rect = pygame.Rect(x-10,y-10,20,20)
        self.state = "normal"
        self.time = 0
        self.dx,self.dy = 0,0
        self.color = "white"
        self.highlight = False
        self.line_length = 0

    def process_click_event(self,pos):
        if self.rect.collidepoint(pos):
            if self.state == "normal":
                self.state = "excited"
            elif self.state == "excited":
                self.state = "normal"

    def check_mouse_close(self,pos):
        self.highlight = self.rect.collidepoint(pos)

    def update(self,dt):
        self.time += dt
            
        if self.state == "normal":
            self.dx,self.dy = 0,0
        elif self.state == "excited":
            self.dx = int(10*(random.random()-0.5))
            self.dy = int(10*(random.random()-0.5))

        if self.highlight:
            self.color = "yellow"
        else:
            self.color = "white"

        # lines graphic
        self.line_length += 0.1*dt
        if self.time > 1000:
            self.time = 0
            self.line_length = 0


    def draw(self,screen):

        # draw expanding lines
        x1 = self.x - self.line_length
        x2 = self.x + self.line_length
        y1 = self.y - self.line_length
        y2 = self.y + self.line_length
        pygame.draw.line(screen,pygame.Color("purple"),(x1,self.y),(x2,self.y))
        pygame.draw.line(screen,pygame.Color("purple"),(self.x,y1),(self.x,y2))

        # draw square
        newrect = (self.rect[0]+self.dx,self.rect[1]+self.dy,*self.rect[2:])
        pygame.draw.rect(screen,pygame.Color(self.color),newrect)
