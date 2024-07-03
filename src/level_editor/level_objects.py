import pygame

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return(f'[{self.x},{self.y}]')

    def new_location(self,x,y):
        self.x = x
        self.y = y

    def close_point(self,pos):
        dist = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
        return(dist < 5)

    def update(self,dt):
        pass

    def draw(self,window,bold=0):
        pygame.draw.rect(window, pygame.Color("yellow"),(self.x-4,self.y-4,9,9),2)

    def highlight(self,window):
        pygame.draw.rect(window, pygame.Color("yellow"),(self.x-6,self.y-6,11,11),4)

class Segment:
    def __init__(self,point):
        self.point1 = point
        self.point2 = None

    def add_star(self,point):
        self.point2 = point
        
    def draw(self,window):
        if self.point1 != None and self.point2 != None:
            points = (self.point1.x,self.point1.y),(self.point2.x,self.point2.y)
            pygame.draw.line(window, pygame.Color("orange"),*points,width=2)
