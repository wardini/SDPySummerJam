import pygame
import random

'''
This simulates a shooting star in the night sky
'''


class ShootingStar:
    def __init__(self,xmin,xmax,ymin,ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.color = pygame.Color(0,0,0)
        self.compute_new_path()
        self.state = "waiting"
        self.head_len = 5
        self.tail_len = 100
        self.speed = 20

    def compute_new_path(self):
        self.startx = int(self.xmin + random.random()*(self.xmax-self.xmin))
        self.starty = int(self.ymin + random.random()*(0.4*(self.ymax-self.ymin)))
        self.endx = int(self.xmin + random.random()*(self.xmax-self.xmin))
        self.endy = int(self.ymin+0.6*(self.ymax-self.ymin)+random.random()*0.4*(self.ymax-self.ymin))
        if self.endx == self.startx:  # to avoid div by 0
            self.endx = self.startx + 3
        self.slope = (self.endy - self.starty) / (self.endx - self.startx)
        self.start_time = int(1000 + 20000*random.random())
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.x3 = -1
        self.y3 = -1
        self.time = 0
        self.length = 0
        self.draw_tail = 0
        self.tail_len = int(50 + random.random()*200)
        self.color.hsva = (random.randrange(0,360),100,30,100)

    def update(self,dt):
        self.time += dt

        if self.state == "waiting":
            if self.time > self.start_time:
                self.x = self.startx
                self.y = self.starty
                self.state = "falling"
                self.length = 0
        elif self.state == "falling":

            # traverse along path until done
            self.length += self.speed

            self.y1 = self.length / (1+self.slope**-2)**0.5 + self.starty
            if self.y1 > self.endy:
                self.state = "waiting"
                self.compute_new_path()
                return

            if self.endx < self.startx:
                self.x1 = -self.length / (1+self.slope**2)**0.5 + self.startx
            else:
                self.x1 = self.length / (1+self.slope**2)**0.5 + self.startx

            self.y2 = (self.length - self.head_len) / (1+self.slope**-2)**0.5 + self.starty
            if self.endx < self.startx:
                self.x2 = -(self.length - self.head_len) / (1+self.slope**2)**0.5 + self.startx
            else:
                self.x2 = (self.length - self.head_len) / (1+self.slope**2)**0.5 + self.startx
            
            self.draw_tail = min(self.tail_len,max(0,self.length - self.head_len))
            if self.draw_tail > 0:
                self.y3 = (self.length - self.head_len - self.draw_tail) / (1+self.slope**-2)**0.5 + self.starty
                if self.endx < self.startx:
                    self.x3 = -(self.length - self.head_len - self.draw_tail) / (1+self.slope**2)**0.5 + self.startx
                else:
                    self.x3 = (self.length - self.head_len - self.draw_tail) / (1+self.slope**2)**0.5 + self.startx


    def draw(self,window):
        if self.state == "falling":
            pygame.draw.line(window,self.color,(self.x1-1,self.y1),(self.x2-1,self.y2))
            pygame.draw.line(window,self.color,(self.x1+1,self.y1),(self.x2+1,self.y2))
            pygame.draw.line(window,self.color,(self.x1,self.y1),(self.x2,self.y2))

            if self.draw_tail > 0:
                pygame.draw.line(window,self.color,(self.x2,self.y2),(self.x3,self.y3))
