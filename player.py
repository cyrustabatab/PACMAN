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
        self.able_to_move = True
        self.score = 0
        self.speed = 2
    


    def get_pixel_position(self):
        return vec(self.grid_pos.x * self.game.cell_width + TOP_BOTTOM_GAP//2 + self.game.cell_width//2,self.grid_pos.y * self.game.cell_height+ TOP_BOTTOM_GAP//2 +self.game.cell_height//2)

    def update(self):

        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.time_to_move():
            if self.stored_direction:
                self.direction = self.stored_direction
                self.stored_direction = None
            self.able_to_move = self.can_move()
        
        self.grid_pos[0],self.grid_pos[1] = (self.pix_pos.x-TOP_BOTTOM_GAP//2)//self.game.cell_width,(self.pix_pos.y - TOP_BOTTOM_GAP)//self.game.cell_height + 1

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.game.screen,PLAYER_COLOR,(int(self.pix_pos.x),int(self.pix_pos.y)),self.game.cell_width//2 -5)
        pygame.draw.rect(self.game.screen,RED,(self.grid_pos[0] * self.game.cell_width + TOP_BOTTOM_GAP//2,self.grid_pos[1] * self.game.cell_height + TOP_BOTTOM_GAP//2,self.game.cell_width,self.game.cell_height),2)
    

    def on_coin(self):
        if self.grid_pos in self.game.coins:
            if int(self.pix_pos.x - self.game.cell_width//2 - 5) % self.game.cell_width == 0:
                if self.direction == vec(1,0) or self.direction == vec(-1,0):
                    return True

            if int(self.pix_pos.y - self.game.cell_height//2 - 5) % self.game.cell_height == 0:
                if self.direction == vec(0,1) or self.direction == vec(0,-1):
                    return True
    

    def eat_coin(self):
        self.game.coins.remove(self.grid_pos)
        self.score += 1

    def move(self,direction):
        self.stored_direction = direction
    
    def time_to_move(self):
        if int(self.pix_pos.x - self.game.cell_width//2 - 5) % self.game.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if int(self.pix_pos.y - self.game.cell_height//2 - 5) % self.game.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True
    
    def can_move(self):
        for wall in self.game.walls:
            if self.grid_pos + self.direction == wall:
                return False

        return True



