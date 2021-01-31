import pygame,random
from settings import *
from collections import deque
from pprint import pprint

vec = pygame.math.Vector2

class Enemy:


    def __init__(self,game,pos,number):
        self.game = game
        self.grid_pos = pos
        self.pixel_pos = self.get_pixel_position()
        self.radius = self.game.cell_width//2.3
        self.number = number
        self.set_color()
        self.direction = vec(2,0)
        self.set_personality()
        self.set_speed()
        self.target = None
        self.create_grid()
    
    def create_grid(self):
        grid = [[0 for j in range(28)] for i in range(30)]


        for cell in self.game.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        
        self.grid = grid

    def get_pixel_position(self):
        return vec(self.grid_pos.x * self.game.cell_width + TOP_BOTTOM_GAP//2 + self.game.cell_width//2,self.grid_pos.y * self.game.cell_height+ TOP_BOTTOM_GAP//2 +self.game.cell_height//2)

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pixel_pos += self.direction * self.speed
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
        if self.personality == 'slow':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'speedy':
            self.direction = self.get_path_direction(self.target)
        if self.personality == 'scared':
            self.direction = self.get_path_direction(self.target)
    

    def get_path_direction(self,target):
        next_cell = self.find_next_cell_in_path(target)
        xdirection = next_cell[0] - self.grid_pos[0]
        ydirection = next_cell[1] - self.grid_pos[1]
        return vec(xdirection,ydirection)


    def find_next_cell_in_path(self,target):

        path = self.bfs((int(self.grid_pos.x),int(self.grid_pos.y)),(int(target.x),int(target.y)))

        next_cell = path[-2]
        return next_cell
    

    def bfs(self,start,target):
        


        queue = deque()
        queue.append(start)

        path = []
        visited = set()

        while queue:
            current = queue.popleft()
            
            visited.add(current)


            if current == target:
                break
            else:
                current_x,current_y = current
                neighbors = ((current_x -1,current_y),(current_x + 1,current_y),(current_x,current_y -1),(current_x,current_y + 1))
                for neighbor_x,neighbor_y in neighbors:
                    if 0 <= neighbor_x < len(self.grid[0]) and 0 <= neighbor_y < len(self.grid):
                        next_cell = (neighbor_x,neighbor_y)
                        if next_cell not in visited:
                            if self.grid[next_cell[1]][next_cell[0]] != 1:
                                #visited.add(next_cell)
                                queue.append(next_cell)
                                path.append({"Current": current,"Next": next_cell})


        shortest = [target]
    

        while target != start:
            for step in path:
                if step['Next']== target:
                    target = step['Current']
                    shortest.append(target)
    
        return shortest

            

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
    
    def set_target(self):
        if self.personality == "speedy" or self.personality == 'slow':
            return self.game.player.grid_pos
        else:
            if self.game.player.grid_pos.x  > COLS//2 and self.game.player.grid_pos.y > ROWS//2:
                return vec(1,1)
            if self.game.player.grid_pos.x  > COLS//2 and self.game.player.grid_pos.y < ROWS//2:
                return vec(1,ROWS -2)
            if self.game.player.grid_pos.x  < COLS//2 and self.game.player.grid_pos.y > ROWS//2:
                return vec(COLS -2,1)
            if self.game.player.grid_pos.x  < COLS//2 and self.game.player.grid_pos.y < ROWS//2:
                return vec(COLS -2,ROWS -2)
            else:
                return vec(COLS -2,ROWS -2)
    

    def set_speed(self):

        if self.personality in ('speedy','scared'):
            self.speed = 2
        else:
            self.speed = 1


    def set_personality(self):

        if self.number == 0:
            self.personality = 'speedy'
            self.direction = vec(1,0)
        elif self.number == 1:
            self.personality = 'slow'
            self.direction = vec(-1,0)
        elif self.number == 2:
            self.personality = 'random'
            self.direction = vec(1,0)
        else:
            self.personality = 'scared'
            self.direction = vec(-1,0)



