import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, personality):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.base_grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.pix_pos_for_animation = self.get_pix_pos_for_animation()
        self.radius = int(self.app.cell_width//2)
        self.personality_and_speed = personality
        self.personality = self.set_personality()
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.target = None
        self.eatable = False  # может быть съеден
        self.eaten = False  # съели
        self.speed = self.set_speed()
        self.image_count = 0


    def update(self):
        self.speed = self.set_speed()
        self.on_base()
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            self.pix_pos_for_animation += self.direction * self.speed
            if self.time_to_move():
                self.move()


        # да (отслеживание по клеткам (так же как и у игрока))
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def now_eatable(self):
        self.eatable = True

    def on_base(self):
        if self.grid_pos == vec(14, 14):
            self.eatable = False
            self.eaten = False
            
    ghost = [pygame.image.load('images/p_57.png'), pygame.image.load('images/p_58.png')]
    
    eye = [pygame.image.load('images/p_59.png'), pygame.image.load('images/p_60.png'),
           pygame.image.load('images/p_61.png'), pygame.image.load('images/p_62.png'),
           pygame.image.load('images/p_63.png'), pygame.image.load('images/p_64.png'),
           pygame.image.load('images/p_65.png'), pygame.image.load('images/p_66.png')]
    
    def draw(self):
        if self.eatable and not self.eaten:
            if self.image_count >= 9:
                self.image_count = 0
            self.app.screen.blit(self.ghost[self.image_count // 5], (int(self.pix_pos_for_animation.x),
                                                                     int(self.pix_pos_for_animation.y)))
            self.image_count += 1

            # здесь призрак должен быть синим, когда просто монетку большую съели
        if self.eaten and self.eatable:
            if self.image_count >= 39:
                self.image_count = 0
            self.app.screen.blit(self.eye[self.image_count // 5], (int(self.pix_pos_for_animation.x),
                                                                   int(self.pix_pos_for_animation.y)))
            self.image_count += 1

            # здесь глазки бегущие на базу
        if not self.eatable and not self.eaten:
            if self.image_count >= 39:
                self.image_count = 0
            self.app.screen.blit(self.colour[self.image_count // 5], (int(self.pix_pos_for_animation.x),
                                                                      int(self.pix_pos_for_animation.y)))
            self.image_count += 1

        #pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def set_speed(self):
        if self.eaten:
            return 1
        elif self.eatable:
            return 0.5
        return self.personality_and_speed["speed"]

    def set_target(self):
        if self.eatable or self.eaten:
            return vec(14, 14)
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(1, 1)  # top left
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)  # bottom left
            if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)  # top right
            else:
                return vec(COLS - 2, ROWS - 2)  # bottom right

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)],
                        [int(target[0]), int(target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for _ in range(28)] for _ in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + current[0] < len(grid[0]):
                        if 0 <= neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        x_dir, y_dir = 0, 0
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            elif number == 1:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return vec(self.grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   self.grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def get_pix_pos_for_animation(self):
        return vec(self.grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
                   self.grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2)

    def set_colour(self):
        if self.personality == "speedy":
            blue = [pygame.image.load('images/p_10.png'), pygame.image.load('images/p_11.png'),
                    pygame.image.load('images/p_12.png'), pygame.image.load('images/p_13.png'),
                    pygame.image.load('images/p_14.png'), pygame.image.load('images/p_15.png'),
                    pygame.image.load('images/p_16.png'), pygame.image.load('images/p_17.png')]
            return blue
        if self.personality == "slow":
            #return 0, 255, 0
            pink = [pygame.image.load('images/p_37.png'), pygame.image.load('images/p_38.png'),
                    pygame.image.load('images/p_39.png'), pygame.image.load('images/p_40.png'),
                    pygame.image.load('images/p_41.png'), pygame.image.load('images/p_42.png'),
                    pygame.image.load('images/p_43.png'), pygame.image.load('images/p_44.png')]
            return pink
        if self.personality == "random":
            #return 255, 0, 0
            red = [pygame.image.load('images/p_29.png'), pygame.image.load('images/p_30.png'),
                   pygame.image.load('images/p_31.png'), pygame.image.load('images/p_32.png'),
                   pygame.image.load('images/p_33.png'), pygame.image.load('images/p_34.png'),
                   pygame.image.load('images/p_35.png'), pygame.image.load('images/p_36.png')]
            return red
        if self.personality == "scared":
            orange = [pygame.image.load('images/p_45.png'), pygame.image.load('images/p_46.png'),
                      pygame.image.load('images/p_47.png'), pygame.image.load('images/p_48.png'),
                      pygame.image.load('images/p_49.png'), pygame.image.load('images/p_50.png'),
                      pygame.image.load('images/p_51.png'), pygame.image.load('images/p_52.png')]
            return orange
            #return 255, 170, 50

    def set_personality(self):
        """
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        elif self.number == 3:
            return "scared"
        """
        return self.personality_and_speed["personality"]
