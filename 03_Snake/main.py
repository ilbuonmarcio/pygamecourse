import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TITLE = 'Snake - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_color = (150, 150, 150) # RGB value

class Snake:

    def __init__(self):
        self.sprite = pygame.image.load('./images/snake_block.png')
        self.rect = self.sprite.get_rect()
        self.curr_x = WIDTH // 2 - self.rect.width // 2
        self.curr_y = HEIGHT // 2 - self.rect.height // 2
        self.tail = []
        self.direction = 'right'
        self.speed = 1 / self.rect.width * 6
        self.unit = self.rect.width

    def move(self):
        if self.direction == 'up':
            self.curr_y -= self.unit * self.speed
        if self.direction == 'down':
            self.curr_y += self.unit * self.speed
        if self.direction == 'left':
            self.curr_x -= self.unit * self.speed
        if self.direction == 'right':
            self.curr_x += self.unit * self.speed

        if self.curr_x > WIDTH:
            self.curr_x = -1 * self.unit
        if self.curr_x + self.unit < 0:
            self.curr_x = WIDTH
        if self.curr_y > HEIGHT:
            self.curr_y = -1 * self.unit
        if self.curr_y + self.unit < 0:
            self.curr_y = HEIGHT

        for block in self.tail:
            if block[0] > WIDTH:
                block[0] = -1 * self.unit
            if block[0] + self.unit < 0:
                block[0] = WIDTH
            if block[1] > HEIGHT:
                block[1] = -1 * self.unit
            if block[1] + self.unit < 0:
                block[1] = HEIGHT


        try:
            del self.tail[len(self.tail)-1]
            self.add_block()
        except:
            pass

        if self.check_if_eating():
            print('eaten!')
            drop_new_apple()
            self.add_block()

    def draw(self):
        pygame.Surface.blit(window, self.sprite, (self.curr_x, self.curr_y))
        for block in self.tail:
            pygame.Surface.blit(window, self.sprite, (block[0], block[1]))

    def add_block(self):
        x, y = self.curr_x, self.curr_y
        if self.direction == 'up':
            y += self.rect.height
        if self.direction == 'down':
            y -= self.rect.height
        if self.direction == 'left':
            x += self.rect.height
        if self.direction == 'right':
            x -= self.rect.height
        self.tail.insert(0, [x + self.unit, y + self.unit])

    def check_if_eating(self):
        global apple_x, apple_y, apple_rect
        if self.curr_x + self.unit > apple_x and \
           self.curr_x + self.unit < apple_x + apple_rect.width and \
           self.curr_y + self.unit > apple_y and \
           self.curr_y + self.unit < apple_y + apple_rect.height:
            return True
        else:
            return False

snake = Snake()

apple_sprite = pygame.image.load('./images/apple.png')
apple_rect = apple_sprite.get_rect()
apple_x = random.randint(0, WIDTH - apple_rect.width)
apple_y = random.randint(0, HEIGHT - apple_rect.height)

def drop_new_apple():
    global apple_x, apple_y
    apple_x = random.randint(0, WIDTH - apple_rect.width)
    apple_y = random.randint(0, HEIGHT - apple_rect.height)

# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    ##### Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break
            if event.key == K_w:
                snake.direction = 'up'
            if event.key == K_s:
                snake.direction = 'down'
            if event.key == K_a:
                snake.direction = 'left'
            if event.key == K_d:
                snake.direction = 'right'

    ##### Game logic
    snake.move()

    ##### Display Rendering
    pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, apple_sprite, (apple_x, apple_y))
    snake.draw()

    ##### Display update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
