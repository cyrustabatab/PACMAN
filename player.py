import pygame
from settings import *
vec = pygame.math.Vector2

class Player:


    def __init__(self,game,pos):
        self.game  = game
        self.grid_pos = pos
        self.pix_pos = self.get_pixel_position()
        self.direction = vec(1,0)
        self.stored_direction = None
    


    def get_pixel_position(self):
        return vec(self.grid_pos.x * self.game.cell_width + TOP_BOTTOM_GAP//2 + self.game.cell_width//2,self.grid_pos.y * self.game.cell_height+ TOP_BOTTOM_GAP//2 +self.game.cell_height//2)

    def update(self):

        self.pix_pos += self.direction
        if self.stored_direction is not None:
            if int(self.pix_pos.x - self.game.cell_width//2 - 5) % self.game.cell_width == 0:
                if self.direction == vec(1,0) or self.direction == vec(-1,0):
                    self.direction = self.stored_direction
                    self.stored_direction = None
        if self.stored_direction is not None:
            if int(self.pix_pos.y - self.game.cell_height//2 - 5) % self.game.cell_height == 0:
                if self.direction == vec(0,1) or self.direction == vec(0,-1):
                    self.direction = self.stored_direction
                    self.stored_direction = None
        self.grid_pos = (self.pix_pos.x-TOP_BOTTOM_GAP//2)//self.game.cell_width,(self.pix_pos.y - TOP_BOTTOM_GAP)//self.game.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.game.screen,PLAYER_COLOR,(int(self.pix_pos.x),int(self.pix_pos.y)),self.game.cell_width//2 -5)
        pygame.draw.rect(self.game.screen,RED,(self.grid_pos[0] * self.game.cell_width + TOP_BOTTOM_GAP//2,self.grid_pos[1] * self.game.cell_height + TOP_BOTTOM_GAP//2,self.game.cell_width,self.game.cell_height),2)


    def move(self,direction):
        self.stored_direction = direction


