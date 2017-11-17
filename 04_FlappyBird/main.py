import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 640, 700
FPS = 60
GAME_TITLE = 'FlappyBird - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_color = (150, 150, 150) # RGB value
space = 240

# https://opengameart.org/content/2d-monster-bat-enemy <-- CC-BY 3.0
bat_images = [
    pygame.image.load('./images/bat/__Bat02_Fly_000.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_001.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_002.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_003.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_004.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_005.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_006.png'),
    pygame.image.load('./images/bat/__Bat02_Fly_007.png'),
]
# https://opengameart.org/content/2d-monster-bat-enemy <-- CC-BY 3.0

wall_down_image = pygame.image.load('./images/wall_down.png')
wall_up_image = pygame.image.load('./images/wall_up.png')

background_image = pygame.image.load('./images/background.png')
background_image = pygame.transform.scale(
    background_image,
    (WIDTH, HEIGHT)
)

vignette_image = pygame.image.load('./images/vignette.png')
vignette_image = pygame.transform.scale(
    vignette_image,
    (WIDTH, HEIGHT)
)

class Bat(pygame.sprite.Sprite):

    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.image = images[0]
        self.images = images
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 6
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.x_gravity = 0
        self.y_gravity = 0.005
        self.x_speed = 0
        self.y_speed = -0.75
        self.animation_delta = 40
        self.animation_counter = 0
        self.animation_current_index = 0

    def move(self, deltatime):
        self.rect.y  += self.y_speed * deltatime
        self.y_speed += self.y_gravity * deltatime
        self.rect.y  += self.y_speed

        if self.rect.y < 0:
            self.rect.y = 0

        self.animate(deltatime)

        self.is_dead()

    def jump(self):
        self.y_speed = -0.75

    def is_dead(self):
        # return
        global game_ended
        if len(pygame.sprite.spritecollide(self, wall_group, False)) > 0:
            game_ended = True
        if self.rect.y > HEIGHT:
            game_ended = True

    def animate(self, deltatime):
        self.animation_counter += deltatime
        if self.animation_counter > self.animation_delta:
            self.animation_counter = 0
            self.animation_current_index += 1
            self.image = self.images[self.animation_current_index % len(self.images)]

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
            move_walls()

class WallUp(Wall):

    def __init__(self, image, x, y):
        Wall.__init__(self, image, x, y)

    def move(self):
        Wall.move(self)
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
            self.rect.y =  HEIGHT // 2 - space // 2 - self.rect.height
            move_walls()

def move_walls():
    delta = random.choice([-60, -30, 30, 60])
    wall_down.rect.y += delta
    wall_up.rect.y += delta

bat = Bat(bat_images)
bat_group = pygame.sprite.GroupSingle(bat)

wall_down = WallDown(
    wall_down_image,
    WIDTH,
    HEIGHT // 2 + space // 2
)

wall_up = WallUp(
    wall_up_image,
    WIDTH,
    HEIGHT // 2 - space // 2 - wall_up_image.get_rect().height
)

wall_group = pygame.sprite.Group(wall_down, wall_up)

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
                bat.jump()

    # Game logic
    bat.move(deltatime)
    for wall in wall_group:
        wall.move()

    # Display update
    # pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, background_image, (0, 0))
    bat_group.draw(window)
    wall_group.draw(window)
    pygame.Surface.blit(window, vignette_image, (0, 0))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
