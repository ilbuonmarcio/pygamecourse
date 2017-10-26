import pygame
import random
from pygame.locals import *

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TITLE = 'Pong - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
pygame.key.set_repeat(10,10)
clock = pygame.time.Clock()

# Game Values

player_sprite = pygame.image.load('./images/player_sprite.png')
player_rect = player_sprite.get_rect()
player_x = 20
player_y = HEIGHT // 2 - player_rect.height // 2

enemy_sprite = pygame.image.load('./images/enemy_sprite.png')
enemy_rect = enemy_sprite.get_rect()
enemy_x = WIDTH - 20 - enemy_rect.width
enemy_y = HEIGHT // 2 - enemy_rect.height // 2

bar_speed = player_y_speed = enemy_y_speed = 15

ball_sprite = pygame.image.load('./images/ball_sprite.png')
ball_rect = ball_sprite.get_rect()
ball_x = WIDTH // 2 - ball_rect.width // 2
ball_y = HEIGHT // 2 - ball_rect.height // 2
ball_x_speed = random.randint(4, 6)
ball_y_speed = random.randint(4, 6)

background_color = (200, 200, 200)

# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    ##### Event handling
    for event in pygame.event.get():

        # Handling keys for closing the game
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break

    # Player's Input Handling
    keys_pressed = pygame.key.get_pressed()

    # Player Input
    if keys_pressed[K_w]:
        player_y -= bar_speed
    if keys_pressed[K_s]:
        player_y += bar_speed

    # Enemy Input
    if keys_pressed[K_o]:
        enemy_y -= bar_speed
    if keys_pressed[K_k]:
        enemy_y += bar_speed

    ##### Game logic
    # Keeping ball into screen
    if ball_x + ball_rect.width >= WIDTH or ball_x <= 0:
        ball_x_speed *= -1
    if ball_y + ball_rect.height >= HEIGHT or ball_y <= 0:
        ball_y_speed *= -1

    # Keeping bars into screen
    if player_y + player_rect.height >= HEIGHT - 20:
        player_y = HEIGHT - player_rect.height - 20
    if player_y < 20:
        player_y = 20

    if enemy_y + enemy_rect.height >= HEIGHT - 20:
        enemy_y = HEIGHT - enemy_rect.height - 20
    if enemy_y < 20:
        enemy_y = 20

    # Moving bar
    ball_x += ball_x_speed
    ball_y += ball_y_speed


    ##### Display Drawing
    pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, player_sprite, (player_x, player_y))
    pygame.Surface.blit(window, enemy_sprite, (enemy_x, enemy_y))
    pygame.Surface.blit(window, ball_sprite, (ball_x, ball_y))

    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
