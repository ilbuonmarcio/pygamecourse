import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 200
GAME_TITLE = 'UnderwaterGravity - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

def scaleimg(image, scale):
    return pygame.transform.scale(image, scale)

def flipimg(image, xbool, ybool):
    return pygame.transform.flip(image, xbool, ybool)

# Edited from https://opengameart.org/content/sky-background
background_image = pygame.image.load('./images/background.png')
background_image = pygame.transform.scale(
    background_image,
    (WIDTH, HEIGHT)
)
# Edited from https://opengameart.org/content/sky-background

player_right_images = [
    scaleimg(pygame.image.load('./images/player/standing0.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/standing1.png'), (64, 64))
]

player_left_images = [
    flipimg(player_right_images[0], True, False),
    flipimg(player_right_images[1], True, False)
]

player_jumping_images = [
    scaleimg(pygame.image.load('./images/player/jump0.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump1.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump2.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump3.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump4.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump5.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump6.png'), (64, 64))
]

player_images = {
    'standing' : player_right_images,
    'right': player_right_images,
    'left' : player_left_images,
    'jumping' : player_jumping_images
}

class Player(pygame.sprite.Sprite):

    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images['right'][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(25, WIDTH - self.rect.width - 25)
        self.rect.y = random.randint(150, HEIGHT - self.rect.height - 25)
        self.x_gravity = 0
        self.y_gravity = 0.001
        self.x_speed = 0
        self.y_speed = 0.03
        self.x_speedmin = -0.5
        self.x_speedmax = 0.5
        self.y_speedmax = 1.5
        self.state = "standing"
        self.previous_state = None
        self.animation_time = 300
        self.jump_animation_time = 100
        self.curr_animation_time = 0
        self.animation_index = 0

    def move(self, deltatime, direction="standing"):

        self.previous_state = self.state
        if direction != "standing":
            self.state = direction

        self.x_speed += self.x_gravity * deltatime
        self.y_speed += self.y_gravity * deltatime

        if direction == "jumping" and self.rect.y > 25:
            self.y_speed = -0.25
        if direction == "left":
            self.x_speed -= 0.01
        if direction == "right":
            self.x_speed += 0.01
        if direction == "standing":
            self.x_speed /= 1.01

        if self.x_speed > self.x_speedmax:
            self.x_speed = self.x_speedmax
        if self.x_speed < self.x_speedmin:
            self.x_speed = self.x_speedmin
        if self.y_speed > self.y_speedmax:
            self.y_speed = self.y_speedmax

        self.rect.y += self.y_speed * deltatime
        self.rect.x += int(self.x_speed * deltatime)

        if self.rect.y + self.rect.height > HEIGHT - 25:
            self.rect.y = HEIGHT - self.rect.height - 25
            if self.state not in ['right', 'left']:
                self.state = "standing"

        if self.rect.x + self.rect.width > WIDTH - 25:
            self.rect.x = WIDTH - self.rect.width - 25

        if self.rect.y < 25:
            self.rect.y = 25

        if self.rect.x < 25:
            self.rect.x = 25

        print("CURRENT STATE: ", self.state)

        self.animate()


    def animate(self):
        print(self.curr_animation_time, self.animation_time)
        if self.previous_state == self.state:
            if self.state != "jumping":
                if self.curr_animation_time >= self.animation_time:
                    self.animation_index += 1
                    self.curr_animation_time = 0
            else:
                if self.curr_animation_time >= self.jump_animation_time:
                    self.animation_index += 1
                    self.curr_animation_time = 0
        else:
            self.animation_index = 0
            self.curr_animation_time = 0

        self.curr_animation_time += deltatime

        self.image = self.images[self.state][self.animation_index % len(self.images[self.state])]


player = Player(player_images)

player_group = pygame.sprite.GroupSingle(player)

background_color = (255, 255, 255) # RGB value

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
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[K_SPACE]:
        player.move(deltatime, "jumping")
    if keys_pressed[K_a]:
        player.move(deltatime, "left")
    if keys_pressed[K_d]:
        player.move(deltatime, "right")

    player.move(deltatime)

    # Display update
    # pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, background_image, (0, 0))

    player_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
