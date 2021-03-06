import pygame,sys,os
from settings import *
from player import Player
from enemy import Enemy

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()


vec = pygame.math.Vector2


class Game:


    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('PACMAN')
        self.clock = pygame.time.Clock()
        self.running = True
        self.new_high_score  = False
        self.state = 'menu' #keep track of what state game is in
        self.cell_width= MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemy_positions = []
        self.load()
        self.coin_count = len(self.coins)
        self.player = Player(self,self.player_position)
        self.make_enemies()
        self.time = 0
        self.death_sound = pygame.mixer.Sound(os.path.join('assets','pacman_death.wav'))
        pygame.mixer.music.load(os.path.join('assets','pacman_beginning.wav'))
        pygame.mixer.music.play(-1)


    





    def run(self):

        

        self.second_event = pygame.USEREVENT + 1 
        pygame.time.set_timer(self.second_event,1000)
        while self.running:
            if self.state == "menu":
                self.menu_events()
                self.menu_update()
                self.menu_draw()
            elif self.state == 'playing':
                self.game_events()
                self.game_update()
                self.game_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'win':
                self.game_over_events()
                self.game_over_update()
                self.win_draw()

            

            

            self.clock.tick(FPS)

        
        pygame.quit()
        sys.exit()
    

    def draw_grid(self):
        
            
        columns= WIDTH//self.cell_width
        for col in range(columns):
            pygame.draw.line(self.background,GRAY,(col * self.cell_width,0),(col*self.cell_width,HEIGHT))
    

        rows = HEIGHT // self.cell_height
        for row in range(rows):
            pygame.draw.line(self.background,GRAY,(0,row * self.cell_height),(WIDTH,row * self.cell_height))
        



        ''' 
        for wall in self.walls:
            pygame.draw.rect(self.background,(112,55,163),(wall.x * self.cell_width,wall.y * self.cell_height,self.cell_width,self.cell_height))
        '''
    

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'playing'
                    pygame.time.set_timer(self.second_event,1000)
                    self.new_high_score = False
                    self.time = 0



    

    def game_over_update(self):
        pass

    

    def win_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(f"YOU WIN!",self.screen,[WIDTH//2,HEIGHT//2],18,RED,MENU_FONT,centered=True)
        if self.new_high_score:
            self.draw_text(f"NEW HIGH SCORE: {self.high_score}",self.screen,[WIDTH//2,HEIGHT//2 + 50],18,RED,MENU_FONT,centered=True)
        pygame.display.update()

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text(f"GAME OVER",self.screen,[WIDTH//2,HEIGHT//2],18,RED,MENU_FONT,centered=True)
        if self.new_high_score:
            self.draw_text(f"NEW HIGH SCORE: {self.high_score}",self.screen,[WIDTH//2,HEIGHT//2 + 50],18,RED,MENU_FONT,centered=True)
        pygame.display.update()





    
    def draw_text(self,text,screen,position,size,color,font_name,centered=False):
        font = pygame.font.SysFont(font_name,size)
        text_surface = font.render(text,False,color)
        text_width,text_height = text_surface.get_size()
        if centered:
            position[0] = position[0] - text_width//2
            position[1] = position[1] - text_height//2
        screen.blit(text_surface,position)
    

    def load(self):
        

        with open('high_score.txt','r') as f:
            self.high_score = int(f.read())

        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background,(MAZE_WIDTH,MAZE_HEIGHT))
        with open('walls.txt','r') as f:
            for y,line in enumerate(f):
                for x,character in enumerate(line):
                    if character == '1':
                        self.walls.append(vec(x,y))
                    elif character == 'C':
                        self.coins.append(vec(x,y))
                    elif character == 'P':
                        self.player_position = (x,y)#vec(x,y)
                    elif character in ('2','3','4','5'):
                        self.enemy_positions.append((x,y))
                    elif character == 'B':
                        pygame.draw.rect(self.background,BLACK,(x * self.cell_width,y * self.cell_height,self.cell_width,self.cell_height))




    def make_enemies(self):

        for i,enemy_position in enumerate(self.enemy_positions):
            self.enemies.append(Enemy(self,enemy_position,i))

    

    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))

            if event.type == self.second_event:
                self.time += 1




    def game_update(self):
        self.player.update()

        for enemy in self.enemies:
            enemy.update()
            if enemy.grid_pos == self.player.grid_pos:
                self.death_sound.play()
                self.remove_life()
        
         
        if self.state != 'game over':
            if self.player.score == self.coin_count:#self.coin_count:
                pygame.time.set_timer(self.second_event,0)
                if self.player.score > self.high_score:
                    self.high_score = self.score
                    self.new_high_score = True
                self.player.overall_reset()
                self.state = 'win'

        


    def game_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background,(TOP_BOTTOM_GAP//2,TOP_BOTTOM_GAP//2))
        self.draw_coins()
        self.draw_grid()
        topleft=(0,0)
        self.draw_text(f"CURRENT SCORE: {self.player.score}",self.screen,(60,1),18,WHITE,MENU_FONT)
        self.draw_text(f"HIGH SCORE: {self.high_score}",self.screen,(WIDTH//2 + 60,1),18,WHITE,MENU_FONT)
        self.draw_text(f"{self.time:>4}",self.screen,(WIDTH - 60,HEIGHT - 25),18,WHITE,MENU_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

        pygame.display.update()

############################## INTRO FUNCTIONS #############################

    def menu_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    self.state = 'playing'
    

    def menu_update(self):
        pass


    def menu_draw(self):
        self.screen.fill(BLACK)
        start_text  = "PUSH SPACE BAR"
        self.draw_text(start_text,self.screen,[WIDTH//2,HEIGHT//2 - 50],MENU_TEXT_SIZE,PUSH_SPACE_BAR_COLOR,MENU_FONT,centered=True)
        one_player_text = "1 PLAYER ONLY"
        self.draw_text(one_player_text,self.screen,[WIDTH//2,HEIGHT//2 + 50],MENU_TEXT_SIZE,(33,137,156),MENU_FONT,centered=True)
        high_score_text = "HIGH SCORE"
        self.draw_text(high_score_text,self.screen,[4,0],MENU_TEXT_SIZE,WHITE,MENU_FONT)

        pygame.display.update()

    
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            pygame.time.set_timer(self.second_event,0)
            if self.player.score > self.high_score:
                self.new_high_score = True
                self.high_score = self.player.score
                with open('high_score.txt','w') as f:
                    f.write(str(self.high_score))
            self.state = 'game over'
            self.player.score = 0

        self.player.reset()
        for enemy in self.enemies:
            enemy.reset()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen,(124,123,7),(coin.x * self.cell_width + self.cell_width//2 + TOP_BOTTOM_GAP//2,coin.y * self.cell_height + self.cell_height//2 + TOP_BOTTOM_GAP//2),5)
