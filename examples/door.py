import pygame

class Door:
    def __init__(self,gridrect,moving_side,untriggered_state,rate):
        self.gridrect = gridrect
        self.moving_side = moving_side
        self.untriggered_state = untriggered_state
        self.last_signal = False
        self.rate = rate
        self.door_graphic = pygame.image.load('graphics/door.png').convert_alpha()
        self.door_sound = pygame.mixer.Sound("sounds/door.ogg")
        self.door_sound.set_volume(1)
        self.reset()

    def reset(self):
        self.door_sound.stop()
        self.last_signal = False
        if self.untriggered_state == 'closed':
            self.curstate = 'closing'
            self.percent_closed = 1.0
            self.gridrect.set_scaled_dx(self.percent_closed,self.moving_side)
        else:
            self.curstate = 'opening'
            self.percent_closed = 0.0
            self.gridrect.set_scaled_dx(self.percent_closed,self.moving_side)

    def update(self,dt):
        if self.curstate == 'opening':
            if self.percent_closed == 0:
                self.door_sound.stop()
                return
            self.percent_closed = max(0.0,self.percent_closed - dt*self.rate/10000)
        elif self.curstate == 'closing':
            if self.percent_closed == 1.0:
                self.door_sound.stop()
                return
            self.percent_closed = min(1.0,self.percent_closed + dt*self.rate/10000)

        if self.moving_side in ['right','left']:
            self.gridrect.set_scaled_dx(self.percent_closed,self.moving_side)
        elif self.moving_side in ['bottom','top']:
            self.gridrect.set_scaled_dy(self.percent_closed,self.moving_side)

    # check if x,y is blocked by the door
    def check_grid(self,x,y):
        return self.gridrect.in_rect(x,y)

    def trigger(self,signal):
        if signal != self.last_signal:
            if signal:
                if self.untriggered_state == 'closed':
                    self.curstate = 'opening'
                else:
                    self.curstate = 'closing'
            else:
                if self.untriggered_state == 'closed':
                    self.curstate = 'closing'
                else:
                    self.curstate = 'opening'
            self.last_signal = signal
            self.door_sound.play(0)

    def render(self,window):
        #self.gridrect.render(window,'orange')
        #window.blit(self.door_graphic,self.gridrect.pgr,(0,0,self.gridrect.dx,self.gridrect.dy))
        if self.moving_side in ['top','left']:
            window.blit(self.door_graphic,self.gridrect.pgr,
                    (0,0,self.gridrect.pgr[2],self.gridrect.pgr[3]))
        else:
            window.blit(self.door_graphic,self.gridrect.pgr,
                    (self.gridrect.dx*16-self.gridrect.pgr[2],
                        self.gridrect.dy*16-self.gridrect.pgr[3],
                        self.gridrect.pgr[2],self.gridrect.pgr[3]))


if __name__ == '__main__':
    from gridrect import GridRect
    import pygame
    from global_items import glbls
    pygame.init()
    screen = pygame.display.set_mode((600,300), flags=pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()

    doorgr1 = GridRect(1,5,20,1)
    doorgr2 = GridRect(1,8,20,1)
    doorgr3 = GridRect(24,1,2,10)
    doorgr4 = GridRect(28,1,3,10)
    doorgr5 = GridRect(1,11,20,1)
    doorgr6 = GridRect(1,14,20,1)
    doorgr7 = GridRect(24,12,2,6)
    doorgr8 = GridRect(28,12,1,6)

    mydoor1 = Door(doorgr1,'right','closed',4)
    mydoor2 = Door(doorgr2,'right','open',14)
    mydoor3 = Door(doorgr3,'bottom','closed',24)
    mydoor4 = Door(doorgr4,'bottom','open',1)
    mydoor5 = Door(doorgr5,'left','closed',4)
    mydoor6 = Door(doorgr6,'left','open',14)
    mydoor7 = Door(doorgr7,'top','closed',24)
    mydoor8 = Door(doorgr8,'top','open',1)

    done = False
    door_trigger = False

    while not done:
        dt = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    door_trigger = not door_trigger
                    mydoor1.trigger(door_trigger)
                    mydoor2.trigger(door_trigger)
                    mydoor3.trigger(door_trigger)
                    mydoor4.trigger(door_trigger)
                    mydoor5.trigger(door_trigger)
                    mydoor6.trigger(door_trigger)
                    mydoor7.trigger(door_trigger)
                    mydoor8.trigger(door_trigger)


        screen.fill(pygame.Color("black"))

        mydoor1.update(dt)
        mydoor2.update(dt)
        mydoor3.update(dt)
        mydoor4.update(dt)
        mydoor5.update(dt)
        mydoor6.update(dt)
        mydoor7.update(dt)
        mydoor8.update(dt)

        mydoor1.render(screen)
        mydoor2.render(screen)
        mydoor3.render(screen)
        mydoor4.render(screen)
        mydoor5.render(screen)
        mydoor6.render(screen)
        mydoor7.render(screen)
        mydoor8.render(screen)

        pygame.display.update()
