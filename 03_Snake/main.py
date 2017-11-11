import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 768, 576
FPS = 10
GAME_TITLE = 'Snake - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
gamefont = pygame.font.SysFont("monospace", 200)
font_color = (255, 255, 255)

# Game Values

background_color = (150, 150, 150) # RGB value

body_image = pygame.image.load('./images/snake_block.png')
head_image = pygame.image.load('./images/snake_head.png')
apple_image = pygame.image.load('./images/apple.png')

# Class for representing the snake
class SnakeHead(pygame.sprite.Sprite):

    # Initialization methon
    def __init__(self, image, snake_tail):
        pygame.sprite.Sprite.__init__(self)
        # Sprite loading
        self.image = image
        self.rect = self.image.get_rect()
        self.snake_tail = snake_tail

        # Current coords and previous coordinates variables
        # initialized to these values
        self.rect.x = random.choice([
            x for x in range(0, WIDTH - self.rect.width, self.rect.width)
        ])
        self.rect.y = random.choice([
            y for y in range(0, HEIGHT - self.rect.height, self.rect.height)
        ])
        self.last_y = None
        self.last_y = None

        self.x_speed = self.rect.width // 2
        self.y_speed = self.rect.height // 2
        self.direction = 'right'

    def move(self):
        # Called every frame, it's responsible for snake's movement
        self.last_x, self.last_y = self.rect.x, self.rect.y

        # Move the snake accordingly to the direction
        if self.direction == 'up':
            self.rect.y -= self.y_speed
        if self.direction == 'down':
            self.rect.y += self.y_speed
        if self.direction == 'left':
            self.rect.x -= self.x_speed
        if self.direction == 'right':
            self.rect.x += self.x_speed

        # Handle going on walls
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y + self.rect.height > HEIGHT:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = HEIGHT - self.rect.height

        self.check_if_eating()

    def add_block(self):
        snake_tail.append(SnakeBody(body_image, self.last_x, self.last_y))
        snake_group = pygame.sprite.Group(self, self.snake_tail)

    def check_if_eating(self):
        for apple in pygame.sprite.spritecollide(self, apple_group, False):
            apple.reset()
            self.add_block()

    def check_if_dead(self):
        pass

class SnakeBody(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Apple(pygame.sprite.Sprite):

    def __init__(self, image, x=None, y=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        if x == None:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
        else:
            self.rect.x = x

        if y == None:
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        else:
            self.rect.y = y

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

snake_tail = []
snake = SnakeHead(head_image, snake_tail)

snake_group = pygame.sprite.Group(snake, *snake_tail)

apple_list = [Apple(apple_image) for _ in range(0, 3)]

apple_group = pygame.sprite.Group(*apple_list)

# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    ##### Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break

            # Snake direction handling
            if event.key == K_w:
                snake.direction = 'up'
            if event.key == K_s:
                snake.direction = 'down'
            if event.key == K_a:
                snake.direction = 'left'
            if event.key == K_d:
                snake.direction = 'right'

    ##### Game Logic
    snake.move()

    ##### Snake Dead
    if snake.check_if_dead():
        game_ended = True

    ##### Display Rendering
    # Drawing the background-color
    pygame.Surface.fill(window, background_color)

    # Drawing the apple
    apple_group.draw(window)

    # Drawing the snake
    snake_group.draw(window)

    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

#Show a 'Game Over' screen
while lose:
    pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, lose_label, (lose_label_x, lose_label_y))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            lose = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                lose = False

pygame.quit()
exit(0)
