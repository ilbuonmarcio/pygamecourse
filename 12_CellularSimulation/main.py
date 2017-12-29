import pygame
from pygame.locals import *
import random
import math

pygame.init()

GAME_RES = WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
FPS = 200
GAME_TITLE = 'Default Game Title'

window = pygame.display.set_mode(GAME_RES, FULLSCREEN|HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_color = (0, 0, 0)

class Cell:

    def __init__(self, ID, dimension, color, x, y, x_speed, y_speed):
        self.ID = ID
        self.dimension = dimension
        self.color = color
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):
        self.x_speed *= random.choice([0.95, 1.05])
        self.y_speed *= random.choice([0.95, 1.05])
        self.x += self.x_speed
        self.y += self.y_speed
        self.x = int(self.x)
        self.y = int(self.y)

        if self.x > WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH
        if self.y > HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT

    def collide(self, other):
        if self.x == other.x and self.y == other.y and self.ID != other.ID:
            global ID_index
            new_cell = Cell(
                ID_index,
                (self.dimension + other.dimension) // 2,
                ((self.color[0] + other.color[0]) // 2, (self.color[1] + other.color[1]) // 2, (self.color[2] + other.color[2]) // 2),
                self.x,
                self.y,
                (self.x_speed + other.x_speed) // 2,
                (self.y_speed + other.y_speed) // 2
            )
            cells.append(new_cell)
            ID_index += 1
            try:
                cells.remove(self)
            except: pass
            try:
                cells.remove(other)
            except: pass

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.dimension, self.dimension))

def recreate_table():
    global num_of_cells, cells
    cells = [
        Cell(
            ID,
            random.randint(8, 16),
            (random.randint(25, 255), random.randint(25, 255), random.randint(25, 255)),
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.randint(-7, 7),
            random.randint(-7, 7)
        ) for ID in range(0, num_of_cells)
    ]

num_of_cells = 128
recreate_table()

ID_index = num_of_cells
# frame_index = 0

# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break
            if event.key == K_SPACE:
                recreate_table()

    # Game logic
    for cell in cells:
        cell.move()

    for cell in cells:
        for other in cells:
            cell.collide(other)

    # Display update
    # pygame.Surface.fill(window, background_color)

    for cell in cells:
        cell.draw(window)

    # pygame.image.save(window, str(frame_index) + ".png")
    # frame_index += 1

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
