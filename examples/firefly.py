import pygame
import random

'''
We create a focal point for the firefly that moves
randomly and slowely in integer steps across the input box.
The firefly x,y accelerates toward this point
'''
class FireFly:
    def __init__(self,minx,miny,maxx,maxy,Nx=100,Ny=10,size=1):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.Nx = Nx
        self.Ny = Ny
        self.fnx = random.randrange(Nx)
        self.fny = random.randrange(Ny)
        self.get_fpoint()
        self.x = self.fx + random.randrange(10) - 5
        self.y = self.fy
        self.vx = 0.01 * (random.random() - 0.5)
        self.vy = 0.01 * (random.random() - 0.5)
        self.repeat_delta = int(600 + 400 * random.random())
        self.time = random.random()*self.repeat_delta
        self.direction = 1
        self.color = pygame.Color(0,0,0)
        self.size = size
        self.ftime = 0
        self.fchange = int(3000 + 2000 * random.random())

    def get_fpoint(self):
        self.fx = int(self.minx + self.fnx*(self.maxx - self.minx)/self.Nx)
        self.fy = int(self.miny + self.fny*(self.maxy - self.miny)/self.Ny)

    def update(self,dt):
        self.time += dt * self.direction
        if self.time > self.repeat_delta:
            self.time = self.repeat_delta
            self.direction = -1
        elif self.time < 0:
            self.time = 0
            self.direction = 1

        c = int(255 * (0.2 + self.time / self.repeat_delta) / 1.2)
        self.color = (c,c,0)

        # move
        a = ((self.x - self.fx)**2 + (self.y - self.fy)**2)**0.5
        tlen = 1000*max(0.1, abs(self.fx - self.x) + abs(self.fy - self.y))
        ax = 0.001 * a * (self.fx - self.x) / tlen
        ay = 0.001 * a * (self.fy - self.y) / tlen

        self.vx = max(min(self.vx + ax,0.04),-0.04)
        self.vy = max(min(self.vy + ay,0.04),-0.04)

        self.x += self.vx * dt
        self.y += self.vy * dt

        # change focal point
        self.ftime += dt
        if self.ftime > self.fchange:
            self.ftime = 0
            self.fnx = max(min(self.fnx + random.randrange(-1,2),self.Nx),0)
            self.fny = max(min(self.fny + random.randrange(-1,2),self.Ny),0)
            self.get_fpoint()


    def draw(self,window):
        #window.set_at((self.x,self.y),self.color)

        pygame.draw.circle(window, self.color, (self.x,self.y), self.size)

        #pygame.draw.aacircle(window, pygame.Color("red"), (self.fx,self.fy), 3)

