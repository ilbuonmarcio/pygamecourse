import pygame
from pygame.locals import *

pygame.init()

GAME_RES = WIDTH, HEIGHT = 1080, 1920
FPS = 60
GAME_TITLE = 'Flappy Bird'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_image = pygame.image.load("./images/Background.png")
count = 1

player_sprite = pygame.image.load('./images/Ghost.png')
player_rect = player_sprite.get_rect()
player_x = WIDTH / 6
player_y = HEIGHT / 2 - player_rect.height / 2

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
        if pygame.mouse.get_pressed()[0]:
            player_y -= HEIGHT / 20
            break

    # Game logic
    count += 1

    #Fill Background
    window.blit(background_image, [0, 0])

    # Ghost Drawing
    pygame.Surface.blit(window, player_sprite, (player_x, player_y))

    # Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
