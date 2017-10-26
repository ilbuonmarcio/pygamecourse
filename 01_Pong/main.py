import pygame
from pygame.locals import *

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TITLE = 'Default Game Title'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

player_x = 20
player_y = 20
player_x_speed = 10
player_y_speed = 10
player_sprite = pygame.image.load('./images/player_sprite.png')

background_color = (200, 200, 200)

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

    # Game logic
    if player_x >= WIDTH-256 or player_x <= 0:
        player_x_speed *= -1

    if player_y >= HEIGHT-256 or player_y <= 0:
        player_y_speed *= -1


    player_x += player_x_speed
    player_y += player_y_speed


    # Display update
    pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, player_sprite, (player_x, player_y))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
