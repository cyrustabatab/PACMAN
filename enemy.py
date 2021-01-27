import pygame
from settings import *

vec = pygame.math.Vector2

class Enemy:


    def __init__(self,game,pos):
        self.game = game
        self.grid_pos = pos
        self.pixel_pos = self.get_pixel_position()

    def get_pixel_position(self):
        return vec(self.grid_pos.x * self.game.cell_width + TOP_BOTTOM_GAP//2 + self.game.cell_width//2,self.grid_pos.y * self.game.cell_height+ TOP_BOTTOM_GAP//2 +self.game.cell_height//2)

    def update(self):
        pass


    def draw(self):
        pygame.draw.circle(self.game.screen,(255,255,255),(int(self.pixel_pos.x),int(self.pixel_pos.y)),15)







