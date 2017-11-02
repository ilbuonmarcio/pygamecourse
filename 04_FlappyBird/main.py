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

class Ghost:

    player_sprite = pygame.image.load('./images/Ghost.png')
    player_rect = player_sprite.get_rect()
    player_x = WIDTH / 6
    player_y = HEIGHT / 2 - player_rect.height / 2
    speed_up = HEIGHT / 10
    speed_down = 15


    def bounce(self):
        for i in range(10):
            self.player_y -= self.speed_up / 10

    def isPressed(self):
        if pygame.mouse.get_pressed()[0]:
            return True


ghost = Ghost()

def physics():
    ghost.player_y += ghost.speed_down

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
        if ghost.isPressed():
            ghost.bounce()
            break

    # Game logic
    physics()

    #Fill Background
    window.blit(background_image, [0, 0])

    # Ghost Drawing
    pygame.Surface.blit(window, ghost.player_sprite, (ghost.player_x, ghost.player_y))

    # Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
