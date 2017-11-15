import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 640, 480
FPS = 60
GAME_TITLE = 'Default Game Title'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_color = (150, 150, 150) # RGB value
space = 120

ghost_image = pygame.image.load('./images/ghost.png')
wall_down_image = pygame.image.load('./images/wall_down.png')
wall_up_image = pygame.image.load('./images/wall_up.png')

class Ghost(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 6
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.x_gravity = 0
        self.y_gravity = 0.005
        self.x_speed = 0
        self.y_speed = -0.75

    def move(self, deltatime):
        self.rect.y  += self.y_speed * deltatime
        self.y_speed += self.y_gravity * deltatime
        self.rect.y  += self.y_speed

        self.is_dead()

    def jump(self):
        self.y_speed = -0.75

    def is_dead(self):
        global game_ended
        if len(pygame.sprite.spritecollide(self, wall_group, False)) > 0:
            game_ended = True

class Wall(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = -6

    def move(self):
        self.rect.x += self.x_speed

class WallDown(Wall):

    def __init__(self, image, x, y):
        Wall.__init__(self, image, x, y)

    def move(self):
        Wall.move(self)
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
            self.rect.y = HEIGHT // 2 + space // 2

class WallUp(Wall):

    def __init__(self, image, x, y):
        Wall.__init__(self, image, x, y)

    def move(self):
        Wall.move(self)
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
            self.rect.y = HEIGHT // 2 + space // 2 - ghost.rect.height - space - self.rect.height


ghost = Ghost(ghost_image)
ghost_group = pygame.sprite.GroupSingle(ghost)

walls = [
    [WallDown(wall_down_image, WIDTH, y), WallUp(wall_up_image, WIDTH, y - ghost.rect.height - space - wall_up_image.get_rect().height)]
    for y in [HEIGHT // 2 + space // 2]
]

walls = sum(walls, [])
wall_group = pygame.sprite.Group(*walls)

# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    deltatime = clock.get_time()

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
            if event.key == K_SPACE:
                ghost.jump()

    # Game logic
    ghost.move(deltatime)
    for wall in wall_group:
        wall.move()

    # Display update
    pygame.Surface.fill(window, background_color)
    ghost_group.draw(window)
    wall_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
