import pygame,random
from settings import *

vec = pygame.math.Vector2

class Enemy:


    def __init__(self,game,pos,number):
        self.game = game
        self.grid_pos = pos
        self.pixel_pos = self.get_pixel_position()
        self.radius = self.game.cell_width//2.3
        self.number = number
        self.set_color()
        self.direction = vec(1,0)
        self.set_personality()


    def get_pixel_position(self):
        return vec(self.grid_pos.x * self.game.cell_width + TOP_BOTTOM_GAP//2 + self.game.cell_width//2,self.grid_pos.y * self.game.cell_height+ TOP_BOTTOM_GAP//2 +self.game.cell_height//2)

    def update(self):
        self.pixel_pos += self.direction
        if self.time_to_move():
            self.move()

        self.grid_pos[0],self.grid_pos[1] = (self.pixel_pos.x-TOP_BOTTOM_GAP//2)//self.game.cell_width,(self.pixel_pos.y - TOP_BOTTOM_GAP)//self.game.cell_height + 1

    def draw(self):
        pygame.draw.circle(self.game.screen,self.color,(int(self.pixel_pos.x),int(self.pixel_pos.y)),self.radius)
    
    def time_to_move(self):
        if int(self.pixel_pos.x - self.game.cell_width//2 - 5) % self.game.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if int(self.pixel_pos.y - self.game.cell_height//2 - 5) % self.game.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True


        return False


    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_direction()
    


    def get_random_direction(self):
        while True:
            number = random.random()
            if number < 0.25:
                x_dir,y_dir = 1,0
            elif number >= 0.25 and number < 0.5:
                x_dir,y_dir = 0,1
            elif number >= 0.5 and number < 0.75:
                x_dir,y_dir = -1,0
            else:
                x_dir,y_dir = 0,-1
            
            direction = vec(x_dir,y_dir)
            if self.grid_pos + direction not in self.game.walls:
                break


        return direction

    def set_color(self):
        if self.number == 0:
            self.color = (42,78,203)
        elif self.number == 1:
            self.color = (197,200,27)
        elif self.number == 2:
            self.color = (189,29,29)
        else:
            self.color = (215,159,33)


    def set_personality(self):

        if self.number == 0:
            self.personality = 'speedy'
        elif self.number == 1:
            self.personality = 'slow'
        elif self.number == 2:
            self.personality = 'random'
        else:
            self.personality = 'scared'



