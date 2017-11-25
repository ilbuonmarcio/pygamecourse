import pygame
from pygame.locals import *

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 550
FPS = 60
GAME_TITLE = 'Importance of DeltaTime - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_color = (200, 200, 200) # RGB value

ball_image = pygame.image.load('./images/ball.png')

class Ball(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = 1
        self.y_speed = 0


class BallDeltaTimed(Ball):

    def __init__(self, image, x, y):
        Ball.__init__(self, image, x, y)

    def move(self, deltatime):
        self.rect.y  += self.y_speed * deltatime
        self.rect.x += self.x_speed * deltatime

        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width

class BallNotDeltaTimed(Ball):

    def __init__(self, image, x, y):
        Ball.__init__(self, image, x, y)

    def move(self, deltatime):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

class FPSSlider(pygame.sprite.Sprite):

    def __init__(self):
        pass

ball_list = [BallNotDeltaTimed(ball_image, WIDTH // 2, 150), BallDeltaTimed(ball_image, WIDTH // 2, 350)]
ball_group = pygame.sprite.Group(*ball_list)

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
    for ball in ball_group:
        ball.move(deltatime)

    # Display update
    pygame.Surface.fill(window, background_color)
    ball_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
