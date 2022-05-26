import pygame.draw
import pygame.math
from settings import *
vec = pygame.math.Vector2
pygame.mixer.init()


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.pix_pos_for_animation = self.get_pix_pos_for_animation()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 1
        self.lives = 1
        self.die = False


    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
            self.pix_pos_for_animation += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # отслеживание по клеткам
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width//2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height//2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

        if self.on_big_coin():
            self.eat_big_coin()
            for enemies in self.app.enemies:
                enemies.now_eatable()

    player_img_left = [pygame.image.load('images/p_4.png'), pygame.image.load('images/p_2.png')]
    player_img_right = [pygame.image.load('images/p_6.png'), pygame.image.load('images/p_8.png')]
    player_img_up = [pygame.image.load('images/p_5.png'), pygame.image.load('images/p_3.png')]
    player_img_down = [pygame.image.load('images/p_9.png'), pygame.image.load('images/p_7.png')]
    player_img_died = [pygame.image.load('images/p_1.png'), pygame.image.load('images/p_18.png'), pygame.image.load('images/p_18.01.png'),
                       pygame.image.load('images/p_19.png'), pygame.image.load('images/p_20.png'),
                       pygame.image.load('images/p_21.png'), pygame.image.load('images/p_22.png'),
                       pygame.image.load('images/p_23.png'), pygame.image.load('images/p_24.png'),
                       pygame.image.load('images/p_25.png'), pygame.image.load('images/p_26.png'),
                       pygame.image.load('images/p_27.png'), pygame.image.load('images/p_28.png')]
    image_count = 0

    def draw_die(self):
        if self.image_count == 116:
            self.image_count = 0
            self.die = False
        if self.die:
            self.app.screen.blit(self.player_img_died[self.image_count // 9], (280, 200))
            self.image_count += 1

    def draw(self):
        if self.image_count == 9:
            self.image_count = 0
        if self.direction == vec(-1, 0): 
            self.image_count += 1
            self.app.screen.blit(self.player_img_left[self.image_count // 5], self.pix_pos_for_animation)
        elif self.direction == vec(1, 0):
            self.image_count += 1
            self.app.screen.blit(self.player_img_right[self.image_count // 5], self.pix_pos_for_animation)
        elif self.direction == vec(0, -1):
            self.image_count += 1
            self.app.screen.blit(self.player_img_up[self.image_count // 5], self.pix_pos_for_animation)
        elif self.direction == vec(0, 1):
            self.app.screen.blit(self.player_img_down[self.image_count // 5], self.pix_pos_for_animation)
            self.image_count += 1
      
        #  pygame.draw.circle(self.app.screen, PLAYER_COLOR, self.pix_pos, self.app.cell_width//2)

        # Прорисовка жизней игрока
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, (35 + 20 * x, HEIGHT - 15), 9)

        # прорисовка хитбокса
            # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER//2,
            #                                        self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER//2,
            #                                        self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        pygame.mixer.music.load('music/credit.wav')
        pygame.mixer.music.play(1)
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def on_big_coin(self):
        if self.grid_pos in self.app.big_coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_big_coin(self):
        pygame.mixer.music.load('music/credit.wav')
        pygame.mixer.music.play(1)
        self.app.big_coins.remove(self.grid_pos)
        self.current_score += 5

    def eat_ghost(self):
        pygame.mixer.music.load('music/credit.wav')
        pygame.mixer.music.play(1)
        self.current_score += 10

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec(self.grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   self.grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def get_pix_pos_for_animation(self):
        return vec(self.grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
                   self.grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2)
   
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
