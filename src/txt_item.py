import pygame

class Txt_item():
    def __init__(self,txt,position,fontsize=18,location="topleft"):
        self.position = position
        self.location = location

        self.font = pygame.font.SysFont('freesansbold',fontsize)
        self.change_text(txt)
        
    def change_text(self,txt):
        self.text = txt
        self.text_surface = self.font.render(self.text, True, pygame.Color("white"))
        if self.location == "topleft":
            self.rect = self.text_surface.get_rect(topleft=(self.position))
        else:
            self.rect = self.text_surface.get_rect(center=(self.position))

    def render_text(self,window):
        window.blit(self.text_surface,self.rect)
