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
gamefont = pygame.font.SysFont("monospace", 30)
font_color = (0, 0, 0)

# Game Values

player_sprite = pygame.image.load('./images/player_sprite.png')
player_rect = player_sprite.get_rect()
player_x = 20
player_y = HEIGHT // 2 - player_rect.height // 2
player_score = 0
player_score_coords = (50, 20)

enemy_sprite = pygame.image.load('./images/enemy_sprite.png')
enemy_rect = enemy_sprite.get_rect()
enemy_x = WIDTH - 20 - enemy_rect.width
enemy_y = HEIGHT // 2 - enemy_rect.height // 2
enemy_score = 0
enemy_score_coords = (WIDTH - 60, 20)

bar_speed = player_y_speed = enemy_y_speed = 15

ball_sprite = pygame.image.load('./images/ball_sprite.png')
ball_rect = ball_sprite.get_rect()
ball_x = WIDTH // 2 - ball_rect.width // 2
ball_y = HEIGHT // 2 - ball_rect.height // 2
ball_x_speed = random.choice((-5, -4, -3, 3, 4, 5))
ball_y_speed = random.choice((-5, -4, -3, 3, 4, 5))

background_color = (200, 200, 200)

# End of Game Values

# Game Functions

def reset_ball():
    global ball_x, ball_y, ball_x_speed, ball_y_speed
    ball_x = WIDTH // 2 - ball_rect.width // 2
    ball_y = HEIGHT // 2 - ball_rect.height // 2
    ball_x_speed = random.choice((-5, -4, -3, 3, 4, 5))
    ball_y_speed = random.choice((-5, -4, -3, 3, 4, 5))

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
    # Move ball
    ball_x += ball_x_speed
    ball_y += ball_y_speed

    # Bouce into bars if collision is made
    if  ball_x >= player_x and \
        ball_x < player_x + player_rect.width and \
        ball_y + ball_rect.height >= player_y and \
        ball_y < player_y + player_rect.height:

        ball_x_speed *= -1
        ball_x = player_x + player_rect.width + 1

    if  ball_x + ball_rect.width >= enemy_x and \
        ball_x + ball_rect.height < enemy_x + enemy_rect.width and \
        ball_y + ball_rect.height >= enemy_y and \
        ball_y < enemy_y + enemy_rect.height:

        ball_x_speed *= -1
        ball_x = enemy_x - ball_rect.width - 1

    # Keeping ball into screen
    if ball_x + ball_rect.width >= WIDTH:
        player_score += 1
        reset_ball()

    if ball_x <= 0:
        enemy_score += 1
        reset_ball()

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

    ##### Display Rendering
    # Score buffer rendering
    player_score_buffer = gamefont.render(str(player_score), 1, font_color)
    enemy_score_buffer = gamefont.render(str(enemy_score), 1, font_color)

    # Window reset
    pygame.Surface.fill(window, background_color)

    # Game elements drawing
    pygame.Surface.blit(window, player_sprite, (player_x, player_y))
    pygame.Surface.blit(window, enemy_sprite, (enemy_x, enemy_y))
    pygame.Surface.blit(window, ball_sprite, (ball_x, ball_y))

    # UI/UX drawing
    pygame.Surface.blit(window, player_score_buffer, player_score_coords)
    pygame.Surface.blit(window, enemy_score_buffer, enemy_score_coords)

    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
