import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TITLE = 'MouseInteractions - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

touchable_images = [
    pygame.image.load('./images/blue.png'),
    pygame.image.load('./images/red.png'),
    pygame.image.load('./images/human.png')
]

for i in range(0, len(touchable_images)):
    touchable_images[i] = pygame.transform.scale(touchable_images[i], (64, 64))

class Touchable(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.x_gravity = 0
        self.y_gravity = 0.003
        self.x_speed = 0
        self.y_speed = -0.75
        self.dragged = False

    def move(self, deltatime, curr_mouse_pos, dragging):
        if dragging:
            temp_mouse_pos = curr_mouse_pos[0] - self.rect.width // 2, curr_mouse_pos[1] - self.rect.height // 2
            if self.rect.collidepoint(temp_mouse_pos) or self.dragged:
                self.rect.x = temp_mouse_pos[0]
                self.rect.y = temp_mouse_pos[1]
                self.dragged = True
            else:
                self.rect.y  += self.y_speed * deltatime
                self.y_speed += self.y_gravity * deltatime
                self.rect.y  += self.y_speed
        else:
            self.dragged = False
            self.rect.y  += self.y_speed * deltatime
            self.y_speed += self.y_gravity * deltatime
            self.rect.y  += self.y_speed

        if self.rect.y + self.rect.height > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
            self.y_speed = random.uniform(-0.9, -0.5)

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = WIDTH - self.rect.width


touchable_objects = [
    Touchable(random.choice(touchable_images)) for i in range(0, 6)
]

touchable_group = pygame.sprite.Group(*touchable_objects)

background_color = (255, 255, 255) # RGB value

curr_mouse_pos = None
dragging = False

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
        if event.type == MOUSEBUTTONDOWN:
            dragging = True
        if event.type == MOUSEBUTTONUP:
            dragging = False
        if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
            curr_mouse_pos = list(pygame.mouse.get_pos())


    # Game logic
    for touchable in touchable_group:
        touchable.move(deltatime, curr_mouse_pos, dragging)

    # Display update
    pygame.Surface.fill(window, background_color)

    touchable_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
