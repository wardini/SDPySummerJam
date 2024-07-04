import pygame
from txt_item import Txt_item
from click_graphic import Click_Graphic
#from level import Level

class Gameplay:
    def __init__(self,glbls):
        self.glbls = glbls
        self.done = False
        self.quit = False
        self.next_state = None

        # load levels
        self.levels = []
        #N = Level.get_levels_count()
        #for i in range(N):
        #    self.levels.append(Level(self.glbls,level_num=i))
        self.cur_level = 0

        # create text items for screen display
        #self.glbls['ti_info1'] = Txt_item('Num Players:' + str(len(self.P)),(0,0),False,None)
        #self.glbls['ti_info1'] = Txt_item(str(len(self.P)),(0,0))
        #self.glbls['ti_wifi'] = Txt_item('Wifi: ' + self.glbls['Try Servername'],(50,0))
        #self.glbls['ti_ip'] = Txt_item('IP Addr: ' + self.glbls['Server IP Address'],(290,0))
        self.glbls['ti_fps'] = Txt_item('00',(self.glbls['WIDTH']-35,0))
        #self.glbls['ti_timer'] = Txt_item(f'Game ends in {self.countdown_time:5.1f} seconds',(220,17))

        self.my_game_element = Click_Graphic(self.glbls['WIDTH']//2,self.glbls['HEIGHT']//2)

        self.play_state = "game"

        self.starpic = pygame.image.load('virgo.png').convert()
        self.forgpic1 = pygame.image.load('foreground1.png').convert_alpha()

    def startup(self):
        self.play_state = "game"

    def update(self,dt):
        self.my_game_element.update(dt)

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_q:
                self.done = True
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.my_game_element.process_click_event(event.pos)

        # highlighting
        self.my_game_element.check_mouse_close(pygame.mouse.get_pos())

    def draw(self, window):
        window.fill(pygame.Color("black"))

        window.blit(self.starpic,self.starpic.get_rect())
        window.blit(self.forgpic1,(0,self.glbls['HEIGHT']-100))
        window.blit(self.forgpic1,(1024,self.glbls['HEIGHT']-100))

        self.glbls['ti_fps'].change_text(str(self.glbls['frame_rate']))
        self.glbls['ti_fps'].render_text(window)

        self.my_game_element.draw(window)
