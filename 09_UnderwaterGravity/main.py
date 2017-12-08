import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 200
GAME_TITLE = 'UnderwaterGravity - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

# Edited from https://opengameart.org/content/sky-background
background_image = pygame.image.load('./images/background.png')
# Edited from https://opengameart.org/content/sky-background

player_image = pygame.image.load('./images/player_0.png')
player_image = pygame.transform.scale(
    player_image,
    (40, 50)
)

class Player(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(25, WIDTH - self.rect.width - 25)
        self.rect.y = random.randint(150, HEIGHT - self.rect.height - 25)
        self.x_gravity = 0
        self.y_gravity = 0.001
        self.x_speed = 0
        self.y_speed = -0.03
        self.x_speedmin = -0.1
        self.y_speedmin = -0.15
        self.x_speedmax = 0.2
        self.y_speedmax = 0.15

    def move(self, deltatime, direction="standing"):

        self.x_speed += self.x_gravity * deltatime
        self.y_speed += self.y_gravity * deltatime

        if direction == "up" and self.rect.y > 25:
            self.y_speed -= 0.035
        if direction == "left":
            self.x_speed -= 0.015
        if direction == "right":
            self.x_speed += 0.015
        if direction == "standing":
            self.x_speed *= 0.994

        if self.x_speed > self.x_speedmax:
            self.x_speed = self.x_speedmax
        if self.x_speed < self.x_speedmin:
            self.x_speed = self.x_speedmin
        if self.y_speed > self.y_speedmax:
            self.y_speed = self.y_speedmax
        if self.y_speed < self.y_speedmin:
            self.y_speed = self.y_speedmin

        self.rect.y += self.y_speed * deltatime
        self.rect.x += self.x_speed * deltatime

        if self.rect.y + self.rect.height > HEIGHT - 25:
            self.rect.y = HEIGHT - self.rect.height - 25

        if self.rect.x + self.rect.width > WIDTH - 25:
            self.rect.x = WIDTH - self.rect.width - 25

        if self.rect.y < 25:
            self.rect.y = 25

        if self.rect.x < 25:
            self.rect.x = 25


player = Player(player_image)

player_group = pygame.sprite.GroupSingle(player)

background_color = (255, 255, 255) # RGB value

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
                break

    # Game logic
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[K_SPACE]:
        player.move(deltatime, "up")
    if keys_pressed[K_a]:
        player.move(deltatime, "left")
    if keys_pressed[K_d]:
        player.move(deltatime, "right")

    player.move(deltatime)

    # Display update
    # pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, background_image, (0, 0))

    player_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
