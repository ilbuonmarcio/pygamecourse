import pygame
from pygame.locals import *
import threading

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 550
FPS = 1000
GAME_TITLE = 'Importance of DeltaTime - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
gamefont = pygame.font.SysFont("monospace", 25)
font_color = (25, 25, 25)

# Game Values

background_color = (200, 200, 200) # RGB value

ball_image = pygame.image.load('./images/ball.png')

ball_deltatimed_label = gamefont.render("BallDeltaTimed", 1, font_color)
ball_notdeltatimed_label = gamefont.render("BallNotDeltaTimed", 1, font_color)

class Ball(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = 1
        self.y_speed = 0

    def move(self, deltatime):
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width


class BallDeltaTimed(Ball):

    def __init__(self, image, x, y):
        Ball.__init__(self, image, x, y)

    def move(self, deltatime):
        Ball.move(self, deltatime)
        self.rect.y  += self.y_speed * deltatime
        self.rect.x += self.x_speed * deltatime

class BallNotDeltaTimed(Ball):

    def __init__(self, image, x, y):
        Ball.__init__(self, image, x, y)

    def move(self, deltatime):
        Ball.move(self, deltatime)
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

def input_handler():
    global FPS
    while True:
        FPS = int(input("Inserisci nuovo valore di FPS: "))

ball_list = [
    BallNotDeltaTimed(ball_image, WIDTH // 2, 150),
    BallDeltaTimed(ball_image, WIDTH // 2, 350)
]
ball_group = pygame.sprite.Group(*ball_list)

t = threading.Thread(target=input_handler)
t.start()

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

    current_fps_label = gamefont.render("FPS: " + str(int(clock.get_fps())), 1, font_color)

    # Display update
    pygame.Surface.fill(window, background_color)
    ball_group.draw(window)

    pygame.Surface.blit(window, current_fps_label, (10, 10))
    pygame.Surface.blit(window, ball_notdeltatimed_label, (200, 100))
    pygame.Surface.blit(window, ball_deltatimed_label, (200, 300))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
