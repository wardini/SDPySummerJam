import pygame

class Txt_item():
    def __init__(self,txt,position,selectable,action,fontsize=28):
        self.text = txt
        self.position = position
        self.selectable = selectable
        self.font = pygame.font.SysFont('timesnewroman',fontsize)
        self.text_surface = self.font.render(self.text, True, pygame.Color("white"))
        self.rect = self.text_surface.get_rect(topleft=(self.position))
        self.action = action
        self.disabled = False
        self.highlighted = False
        
    def change_text(self,txt):
        self.text = txt
        self.text_surface = self.font.render(self.text, True, pygame.Color("white"))
        self.rect = self.text_surface.get_rect(topleft=(self.position))

    def highlight(self):
        self.highlighted = True

    def unhighlight(self):
        self.highlighted = False

    def render_text(self,screen):
        screen.blit(self.text_surface,self.rect)
        if self.selectable:
            if self.disabled:
                pygame.draw.rect(screen, pygame.Color("gray20"),(self.rect[0]-4,self.rect[1]-4,self.rect[2]+8,self.rect[3]+4),2)
            else:
                if self.highlighted:
                    pygame.draw.rect(screen, pygame.Color("white"),(self.rect[0]-4,self.rect[1]-4,self.rect[2]+8,self.rect[3]+4),4)
                else:
                    pygame.draw.rect(screen, pygame.Color("white"),(self.rect[0]-4,self.rect[1]-4,self.rect[2]+8,self.rect[3]+4),2)

    def disable_click(self):
        self.text_surface = self.font.render(self.text, True, pygame.Color("gray20"))
        self.rect = self.text_surface.get_rect(topleft=(self.position))
        self.disabled = True

    def check_select(self,pos):
        if self.selectable and not self.disabled:
            return(self.rect.collidepoint(pos))
        else:
            return(False)
