import pygame
from pygame.locals import *
from random import randint as ri
import copy

pygame.init()

GAME_RES = WIDTH, HEIGHT = 480, 480
FPS = 60
GAME_TITLE = 'Game of Life - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values
background_color = (0, 0, 0)
cell_color = (255, 255, 255)
cell_dim = 10

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = ri(0, 1)

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y) for x in range(0, width)] for y in range(0, height)
        ]

    def drop_new_cells(self):
        self.grid = [
            [Cell(x, y) for x in range(0, self.width)] for y in range(0, self.height)
        ]

    def apply_rules(self):
        futuregrid = copy.deepcopy(self.grid)
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                s = 0

                try: s += self.grid[x - 1][y - 1].state;
                except: pass

                try: s += self.grid[x][y - 1].state
                except: pass

                try: s += self.grid[x + 1][y - 1].state
                except: pass

                try: s += self.grid[x - 1][y].state
                except: pass

                try: s += self.grid[x + 1][y].state
                except: pass

                try: s += self.grid[x - 1][y + 1].state
                except: pass

                try: s += self.grid[x][y + 1].state
                except: pass

                try: s += self.grid[x + 1][y + 1].state
                except: pass

                if self.grid[x][y].state == 1 and (s < 2 or s > 3):
                    futuregrid[x][y].state = 0
                elif self.grid[x][y].state == 0 and s == 3:
                    futuregrid[x][y].state = 1

        self.grid = futuregrid

    def draw(self, surface):
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[0])):
                if self.grid[x][y].state == 1:
                    pygame.draw.rect(surface, cell_color, (
                        self.grid[x][y].x * cell_dim,
                        self.grid[x][y].y * cell_dim,
                        cell_dim,
                        cell_dim
                        )
                    )

grid = Grid(WIDTH // cell_dim, HEIGHT // cell_dim)

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
                grid.drop_new_cells()

    # Game logic
    grid.apply_rules()

    # Display update
    pygame.Surface.fill(window, background_color)
    grid.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
