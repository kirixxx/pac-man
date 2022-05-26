import json
import sys
import pygame_widgets
from pygame_widgets.button import Button
from player_class import *
from enemy_class import *
from leaders_class import Leader

pygame.init()
pygame.mixer.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #pygame.display.set_caption('pacman')
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.big_coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.ghost_personalities = None
        self.background = None

        with open("data_file.json", "r") as read_file:
            self.leaders_list = json.load(read_file)
        self.lead = Leader(self.leaders_list)

        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
     

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            elif self.state == 'rules':
                self.rules_events()
                self.draw_rules()

            elif self.state == 'hs_table':
                self.hs_table_events()
                self.draw_hs_table()

            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            
            elif self.state == 'win':
                self.draw_win()
                self.win_events()

            elif self.state == 'exit':
                pygame.quit()
                sys.exit()

            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ############################# Помогающие функции ###################################


    def draw_text(self, words, screen, position, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            position[0] = position[0] - text_size[0]//2
            position[1] = position[1] - text_size[1]//2
        screen.blit(text, position)

    def load(self):
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Загрузка карты с фалйа
        # Создание стен с координатами
        with open("walls.txt", 'r') as file:
            for yIdx, line in enumerate(file):
                for xIdx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xIdx, yIdx))
                    elif char == 'C':
                        self.coins.append(vec(xIdx, yIdx))
                    elif char == 'X':
                        self.big_coins.append(vec(xIdx, yIdx))
                    elif char == 'P':
                        self.p_pos = [xIdx, yIdx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xIdx, yIdx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xIdx*self.cell_width, yIdx*self.cell_width,
                                                                  self.cell_width, self.cell_height))
        # print(self.walls)

    def make_enemies(self):
        with open('ghost_personality.json') as personalities:
            self.ghost_personalities = json.load(personalities)
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), self.ghost_personalities[idx]))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))

        #for coin in self.coins:
        #    pygame.draw.rect(self.background, (255, 200, 0), (coin.x * self.cell_width, coin.y * self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.player.lives = 1
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.pix_pos_for_animation = self.player.get_pix_pos_for_animation()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.pix_pos_for_animation = enemy.get_pix_pos_for_animation()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"
        
    def add_button_play(self, h, w):
        button_play = Button(self.screen,
                             h,
                             w,
                             200,
                             45,
                             text='playing',
                             textColour=PLAYER_COLOR,
                             font=pygame.font.Font('fonts/emulogic.ttf', 23),
                             fontSize=23,
                             margin=20,
                             inactiveColour=BLACK,
                             hoverColour=BLUE,
                             pressedColour=BLUE,
                             onClick=self.button_play)
    
    def add_button_hs_table(self, h, w):
        button_hs_table = Button(self.screen,
                                 h,
                                 w,
                                 200,
                                 45,
                                 text='hs table',
                                 textColour=PLAYER_COLOR,
                                 font=pygame.font.Font('fonts/emulogic.ttf', 23),
                                 fontSize=23,
                                 margin=20,
                                 inactiveColour=BLACK,
                                 hoverColour=BLUE,
                                 pressedColour=BLUE,
                                 onClick=self.button_hs_table)
    
    def add_button_rules(self, h, w):
        button_rules = Button(self.screen,
                              h,
                              w,
                              200,
                              45,
                              text='rules',
                              textColour=PLAYER_COLOR,
                              font=pygame.font.Font('fonts/emulogic.ttf', 23),
                              fontSize=23,
                              margin=20,
                              inactiveColour=BLACK,
                              hoverColour=BLUE,
                              pressedColour=BLUE,
                              onClick=self.button_rules)
    
    def add_button_exit(self, h, w):
        button_exit = Button(self.screen,
                             h,
                             w,
                             200,
                             45,
                             text='exit',
                             textColour=PLAYER_COLOR,
                             font=pygame.font.Font('fonts/emulogic.ttf', 23),
                             fontSize=23,
                             margin=20,
                             inactiveColour=BLACK,
                             hoverColour=BLUE,
                             pressedColour=BLUE,
                             onClick=self.button_exit)
    
    def add_button_back(self, h, w):
        button_back = Button(self.screen,
                             h,
                             w,
                             200,
                             45,
                             text='back',
                             textColour=PLAYER_COLOR,
                             font=pygame.font.Font('fonts/emulogic.ttf', 23),
                             fontSize=23,
                             margin=20,
                             inactiveColour=BLACK,
                             hoverColour=BLUE,
                             pressedColour=BLUE,
                             onClick=self.button_back)
        
    def add_button_play_again(self, h, w):
        button_play_again = Button(self.screen,
                                   h,
                                   w,
                                   220,
                                   45,
                                   text='play again',
                                   textColour=PLAYER_COLOR,
                                   font=pygame.font.Font('fonts/emulogic.ttf', 23),
                                   fontSize=23,
                                   margin=20,
                                   inactiveColour=BLACK,
                                   hoverColour=BLUE,
                                   pressedColour=BLUE,
                                   onClick=self.button_play_again)
        
    def button_play_again(self):
        self.reset()
        
    def button_back(self):
        self.state = 'start'
        
    def button_exit(self):
        self.state = 'exit'
        
    def button_play(self):
        pygame.mixer.music.load('music/game_start.wav')
        pygame.mixer.music.play(1)
        self.state = 'playing'
    
    def button_hs_table(self):
        self.state = 'hs_table'
    
    def button_rules(self):
        self.state = 'rules'


    ############################# Функции для интро ###################################


    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            '''
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.load('music/game_start.wav')
                pygame.mixer.music.play(1)
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.state = 'rules'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                self.state = 'hs_table'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'exit'
            '''
            pygame_widgets.WidgetHandler._widgets.clear()

    def start_update(self):
        self.add_button_rules(WIDTH/2 - 100, HEIGHT - 260)
        self.add_button_exit(WIDTH/2 - 100, HEIGHT - 190)
        self.add_button_play(WIDTH/2 - 100, HEIGHT - 400)
        self.add_button_hs_table(WIDTH/2 - 100, HEIGHT - 330)
        #pass

    def start_draw(self):
        self.screen.fill(BLACK)
        name = pygame.image.load('images/name.png')
        self.screen.blit(name, (70, 50))
        '''  
        self.draw_text('Play - space bar', self.screen, [WIDTH//2, HEIGHT//2 - 50], START_TEXT_SIZE,
                       (255, 185, 33), START_FONT, centered=True)
        self.draw_text('How to play - R', self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE,
                       (188, 255, 33), START_FONT, centered=True)
        self.draw_text('High score table - T', self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE,
                       (48, 255, 33), START_FONT, centered=True)
        self.draw_text('Exit - Esc', self.screen, [WIDTH // 2, HEIGHT // 2 + 100], START_TEXT_SIZE,
                       (33, 255, 137), START_FONT, centered=True)
        '''
        events = pygame.event.get()
        pygame_widgets.update(events)
        pygame.display.update() 

    ############################# Функции для игры ###################################
    player_img = list()

    def playing_events(self):
        self.player_img = self.player.player_img_right
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1)) 
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0)) 


    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                if enemy.eatable:
                    if not enemy.eaten:
                        self.player.eat_ghost()
                        enemy.eaten = True
                    break
                self.player.die = True
                self.remove_life()
               
    def playing_draw(self): 
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
    
        self.draw_coins()
        self.draw_big_coins()
        # self.draw_grid()
        self.draw_text('Current score: {}'.format(self.player.current_score), self.screen, [50, 0], 16, WHITE, START_FONT)
        self.draw_text('High score: {}'.format(self.leaders_list[len(self.leaders_list) - 1]["result"]), self.screen, [WIDTH//2 + 150, 0], 16, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        
        

    def remove_life(self):
        self.player.lives -= 1
        pygame.mixer.music.load('music/death_1.wav')
        pygame.mixer.music.play(1)
        if self.player.lives == 0:
            if self.player.current_score < self.leaders_list[len(self.leaders_list) - 1]["result"]:
                self.state = 'game over'
            elif self.player.current_score > self.leaders_list[len(self.leaders_list) - 1]["result"]:
                self.state = 'win'
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.pix_pos_for_animation = self.player.get_pix_pos_for_animation()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.pix_pos_for_animation = enemy.get_pix_pos_for_animation()
                enemy.direction *= 0


    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (200, 200, 10),
                               (int(coin.x * self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                int(coin.y * self.cell_height) + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 3)

    def draw_big_coins(self):
        for coin in self.big_coins:
            pygame.draw.circle(self.screen, (200, 200, 10),
                               (int(coin.x * self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                int(coin.y * self.cell_height) + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 8)


    ############################# Функции для правил ###################################


    def rules_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'start'
        pygame_widgets.WidgetHandler._widgets.clear()

    def draw_rules(self):
        self.screen.fill(BLACK)
        player_img = pygame.image.load('images/p_6.png')
        opponent = pygame.image.load('images/p_10.png')
        opponent_1 = pygame.image.load('images/p_39.png')
        opponent_2 = pygame.image.load('images/p_49.png')
        self.draw_text('Rules', self.screen, [WIDTH//2, 50], START_TEXT_SIZE,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text('Your task is to collect as many points <<', self.screen, [20, 80], 26, WHITE, START_FONT)
        pygame.draw.circle(self.screen, (200, 200, 10), (520, 100), 10)
        self.draw_text('>> as', self.screen, [540, 80], 26, WHITE, START_FONT)
        self.draw_text('possible by controlling the Pacman << ', self.screen, [20, 110], 26, WHITE, START_FONT)
        self.screen.blit(player_img, (470, 120))
        self.draw_text('>> using', self.screen, [495, 110], 26, WHITE, START_FONT)
        self.draw_text('the arrows on the keyboard << ', self.screen, [20, 140], 26, WHITE, START_FONT)
        keyboard_1 = pygame.image.load('images/p_53.bmp')
        self.screen.blit(keyboard_1, (390, 150))
        self.draw_text('>>', self.screen, [420, 140], 26, WHITE, START_FONT)
        keyboard_1 = pygame.image.load('images/p_54.png')
        self.draw_text(', <<', self.screen, [450, 140], 26, WHITE, START_FONT)
        self.screen.blit(keyboard_1, (490, 150))
        self.draw_text('>>,', self.screen, [515, 140], 26, WHITE, START_FONT)
        self.draw_text('<<', self.screen, [20, 170], 26, WHITE, START_FONT)
        keyboard_1 = pygame.image.load('images/p_55.png')
        self.screen.blit(keyboard_1, (55, 180))
        self.draw_text('>>,', self.screen, [80, 170], 26, WHITE, START_FONT)
        self.draw_text('<<', self.screen, [110, 170], 26, WHITE, START_FONT)
        keyboard_1 = pygame.image.load('images/p_56.bmp')
        self.screen.blit(keyboard_1, (145, 180))
        self.draw_text('>>', self.screen, [174, 170], 26, WHITE, START_FONT)
        self.draw_text('and avoiding opponents <<', self.screen, [200, 170], 26, WHITE, START_FONT)
        self.screen.blit(opponent_2, (515, 180))
        self.draw_text('>>,', self.screen, [545, 170], 26, WHITE, START_FONT)
        self.draw_text('<<', self.screen, [20, 200], 26, WHITE, START_FONT)
        self.screen.blit(opponent_1, (50, 210))
        self.draw_text('>>,', self.screen, [80, 200], 26, WHITE, START_FONT)
        self.draw_text('<<', self.screen, [110, 200], 26, WHITE, START_FONT)
        self.screen.blit(opponent, (140, 210))
        self.draw_text('>>.', self.screen, [170, 200], 26, WHITE, START_FONT)
        #self.draw_text('back to main menu - esc', self.screen, [50, 630],13, WHITE, START_FONT)
        #self.draw_text('play - space bar', self.screen, [WIDTH//2 + 150, 630], 13, WHITE, START_FONT)
        self.add_button_back(50, 600)
        self.add_button_play(370, 600)
        events = pygame.event.get()
        pygame_widgets.update(events)
        pygame.display.update()


    ############################# Функции для таблицы рекордов ###################################


    def hs_table_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'start' 
        pygame_widgets.WidgetHandler._widgets.clear()
           
    def draw_hs_table(self):
        self.screen.fill(BLACK)       
        self.draw_text('Leaders', self.screen, [WIDTH//2, 50], START_TEXT_SIZE,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text('Names:', self.screen, [150, 80], 16, WHITE, START_FONT)
        self.draw_text('Results:', self.screen, [340, 80], 16, WHITE, START_FONT)
        self.draw_text('_____________________________________________________', self.screen, [40, 90], 16, WHITE, START_FONT)
        count = 110
        for i in range(len(self.leaders_list)-1, -1, -1):
            if i == len(self.leaders_list) - 1:
                color = PLAYER_COLOR
            else:
                color = WHITE
            #print(str(self.leaders_list[i]["name"]) +"   " +str(self.leaders_list[i]["result"]))
            self.draw_text(str(self.leaders_list[i]["name"]), self.screen, [150, count], 16,  color, START_FONT)
            self.draw_text(str(self.leaders_list[i]["result"]), self.screen, [350, count], 16,  color, START_FONT)
            self.draw_text('_____________________________________________________', self.screen, [40, count + 15], 16, WHITE, START_FONT)
            count += 40
        self.add_button_back(50, 600)
        self.add_button_play(370, 600)
        events = pygame.event.get()
        pygame_widgets.update(events)
        pygame.display.update()


    ############################# Функции для проигрыша ###################################


    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False   
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #   self.reset()
            ''''
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'exit'
            '''
            pygame_widgets.WidgetHandler._widgets.clear()
            

    def game_over_update(self):
        #self.add_button_exit(WIDTH // 2 - 120, HEIGHT// 1.5 )
        #self.add_button_play(WIDTH // 2 - 120, HEIGHT// 2 )
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        pygame_widgets.WidgetHandler._widgets.clear()
        '''
        quit_text = "Escape - quit"
        again_text = "Space - play again"
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100], 52, RED, START_FONT, centered=True)
        self.draw_text(again_text, self.screen, [WIDTH//2, HEIGHT//2], 36, (189, 189, 189), START_FONT, centered=True)
        self.draw_text(quit_text, self.screen, [WIDTH//2, HEIGHT//1.5], 36, (189, 189, 189), START_FONT, centered=True)
        '''
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100], 52, RED, START_FONT, centered=True)
        self.player.draw_die()
        self.add_button_exit(WIDTH // 2 - 100, HEIGHT//1.5)
        self.add_button_play_again(WIDTH // 2 - 110, HEIGHT//2)
        events = pygame.event.get()
        pygame_widgets.update(events)
        pygame.display.update()

    ############################# Функции для победы ###################################

    def print_text(self, text, n):
        self.draw_text('New record', self.screen, [WIDTH//2, 50], 2 * START_TEXT_SIZE,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text(str(self.player.current_score), self.screen, [WIDTH//2, 130],  2 * START_TEXT_SIZE - 10,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text(str(text), self.screen, [20 + 20*n, 200], START_TEXT_SIZE,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text("__", self.screen, [20 + 20*n, 200], START_TEXT_SIZE,
                       PLAYER_COLOR, START_FONT, centered=True)
        pygame.display.update()

    def draw_win(self):
        self.screen.fill(BLACK) 
        self.draw_text('New record', self.screen, [WIDTH//2, 50], 2 * START_TEXT_SIZE,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text(str(self.player.current_score), self.screen, [WIDTH//2, 130], 2 * START_TEXT_SIZE - 10,
                       PLAYER_COLOR, START_FONT, centered=True)
        self.draw_text('Enter a name', self.screen, [WIDTH//2 - 100, 200], START_TEXT_SIZE,
                       GREY, START_FONT, centered=True)
    
        pygame.display.update()
        
    def win_events(self):
        self.screen.fill(BLACK) 
        n = 1
        show = True
        need_input = True
        input_text = ''
        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if need_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        show = False
                        need_input = False
                        self.lead.add_to_list(str(input_text), self.player.current_score)
                        self.leaders_list = self.lead.add_to_list(str(input_text), self.player.current_score)
                        self.reset()
                        self.state = 'hs_table'
                    elif event.key == pygame.K_BACKSPACE:
                        pass
                    else:
                        
                        input_text += event.unicode 
                        n += 1
                        self.print_text(str(event.unicode), n)
        
        pygame.display.update()
        self.clock.tick(60)
