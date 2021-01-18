import pygame,sys
from settings import *


pygame.init()


vec = pygame.math.Vector2


class Game:


    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'menu' #keep track of what state game is in


    def run(self):


        while self.running:
            if self.state == "menu":
                self.menu_events()
                self.menu_update()
                self.menu_draw()
            

            

            self.clock.tick(FPS)

        
        pygame.quit()
        sys.exit()
 
    
    def draw_text(self,text,screen,position,size,color,font_name):
        font = pygame.font.SysFont(font_name,size)
        text_surface = font.render(text,False,color)
        text_width,text_height = text_surface.get_size()
        position[0] = position[0] - text_width//2
        position[1] = position[1] - text_height//2
        screen.blit(text_surface,position)


############################## INTRO FUNCTIONS #############################

    def menu_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'playing'
    

    def menu_update(self):
        pass


    def menu_draw(self):
        self.screen.fill(BLACK)
        start_text  = "PUSH SPACE BAR"
        self.draw_text(start_text,self.screen,[WIDTH//2,HEIGHT//2],MENU_TEXT_SIZE,PUSH_SPACE_BAR_COLOR,MENU_FONT)
        pygame.display.update()
