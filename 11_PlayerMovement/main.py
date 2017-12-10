import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 200
GAME_TITLE = 'PlayerMovement - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

def scaleimg(image, scale):
    return pygame.transform.scale(image, scale)

def flipimg(image, xbool, ybool):
    return pygame.transform.flip(image, xbool, ybool)

# Edited from https://opengameart.org/content/dark-night-full-moon-background
background_image = pygame.image.load('./images/background.png')
background_image = pygame.transform.scale(
    background_image,
    (WIDTH, HEIGHT)
)
# Edited from https://opengameart.org/content/dark-night-full-moon-background

parachute_image = scaleimg(pygame.image.load('./images/player/parachute.png'), (64, 64))

# Edited from https://opengameart.org/content/high-res-fire-ball
projectile_left_images = [
    scaleimg(pygame.image.load('./images/red.png'), (72, 32)),
    scaleimg(pygame.image.load('./images/pink.png'), (72, 32)),
    scaleimg(pygame.image.load('./images/blue.png'), (72, 32))
]

projectile_right_images = [
    flipimg(projectile_left_images[0], True, False),
    flipimg(projectile_left_images[1], True, False),
    flipimg(projectile_left_images[2], True, False)
]
# Edited from https://opengameart.org/content/high-res-fire-ball

player_right_images = [
    scaleimg(pygame.image.load('./images/player/standing0.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/standing1.png'), (64, 64))
]

player_left_images = [
    flipimg(player_right_images[0], True, False),
    flipimg(player_right_images[1], True, False)
]

player_jumping_right_images = [
    scaleimg(pygame.image.load('./images/player/jump0.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump1.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump2.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump3.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump4.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump5.png'), (64, 64)),
    scaleimg(pygame.image.load('./images/player/jump6.png'), (64, 64))
]

player_jumping_left_images = [
    flipimg(player_jumping_right_images[0], True, False),
    flipimg(player_jumping_right_images[1], True, False),
    flipimg(player_jumping_right_images[2], True, False),
    flipimg(player_jumping_right_images[3], True, False),
    flipimg(player_jumping_right_images[4], True, False),
    flipimg(player_jumping_right_images[5], True, False),
    flipimg(player_jumping_right_images[6], True, False)
]

player_images = {
    'right': player_right_images,
    'left' : player_left_images,
    'jumping_left' : player_jumping_left_images,
    'jumping_right' : player_jumping_right_images
}

class Parachute(pygame.sprite.Sprite):

    def __init__(self, image=parachute_image):
        pygame.sprite.Sprite.__init__(self)
        self.image_reference = image
        self.blank_image = pygame.Surface((64, 64))
        self.blank_image.set_alpha(0)
        self.image = self.blank_image
        self.rect = self.image.get_rect()

    def toggle(self, value, x, y):
        self.rect.x = x
        self.rect.y = y - 32
        if value:
            self.image = self.image_reference
        else:
            self.image = self.blank_image

class Projectile(pygame.sprite.Sprite):

    def __init__(self, image, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.x_speed = 1
        self.y_speed = random.choice(
            [n * 0.03 for n in range(-10, 10, 1)]
        )

    def move(self, deltatime):
        self.rect.x += self.x_speed * deltatime * self.direction
        self.rect.y += self.y_speed * deltatime

        if self.rect.x > WIDTH or self.rect.x < -self.rect.width \
           or self.rect.y > HEIGHT or self.rect.y < -self.rect.height:
           projectile_group.remove(self)

class Player(pygame.sprite.Sprite):

    def __init__(self, images, parachute):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images['right'][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(25, WIDTH - self.rect.width - 25)
        self.rect.y = random.randint(150, HEIGHT - self.rect.height - 25)
        self.x_gravity = 0
        self.y_gravity = 0.003
        self.x_speed = 0
        self.y_speed = 0.03
        self.x_speedmin = -0.5
        self.x_speedmax = 0.5
        self.y_speedmin = -0.8
        self.y_speedmax = 1.5
        self.state = "right"
        self.previous_state = None
        self.animation_time = 300
        self.jump_animation_time = 100
        self.curr_animation_time = 0
        self.animation_index = 0
        self.parachute = parachute
        self.cast_time = 20
        self.curr_cast_time = 0

    def move(self, deltatime, actions=[]):

        self.previous_state = self.state

        if "left" in actions and "jump" in actions:
            self.x_speed -= 0.03
            self.y_speed -= 0.075
            self.state = "jumping_left"
            self.parachute.toggle(True, self.rect.x, self.rect.y)
        elif "right" in actions and "jump" in actions:
            self.x_speed += 0.03
            self.y_speed -= 0.075
            self.state = "jumping_right"
            self.parachute.toggle(True, self.rect.x, self.rect.y)
        elif "jump" in actions:
            self.y_speed -= 0.075
            if self.previous_state == "right":
                self.state = "jumping_right"
            if self.previous_state == "left":
                self.state = "jumping_left"
            self.parachute.toggle(True, self.rect.x, self.rect.y)
        elif "left" in actions:
            self.x_speed -= 0.03
            self.state = "left"
            self.parachute.toggle(False, self.rect.x, self.rect.y)
        elif "right" in actions:
            self.x_speed += 0.03
            self.state = "right"
            self.parachute.toggle(False, self.rect.x, self.rect.y)
        elif len(actions) == 0:
            self.state = self.previous_state
            self.x_speed *= 0.93
            self.parachute.toggle(False, self.rect.x, self.rect.y)

        if self.x_speed < self.x_speedmin:
            self.x_speed = self.x_speedmin
        if self.x_speed > self.x_speedmax:
            self.x_speed = self.x_speedmax
        if self.y_speed < self.y_speedmin:
            self.y_speed = self.y_speedmin
        if self.y_speed > self.y_speedmax:
            self.y_speed = self.y_speedmax


        self.x_speed += self.x_gravity * deltatime
        self.y_speed += self.y_gravity * deltatime

        self.rect.y += int(self.y_speed * deltatime)
        self.rect.x += int(self.x_speed * deltatime)

        if self.rect.y + self.rect.height > HEIGHT - 25:
            self.rect.y = HEIGHT - self.rect.height - 25
            self.y_speed = 0
            if self.state == "jumping_left":
                self.state = "left"
            elif self.state == "jumping_right":
                self.state = "right"

        if self.rect.x + self.rect.width > WIDTH - 25:
            self.rect.x = WIDTH - self.rect.width - 25

        if self.rect.y < 25:
            self.rect.y = 25

        if self.rect.x < 25:
            self.rect.x = 25

        # print("CURRENT STATE: ", self.state)

        self.animate()


    def animate(self):
        # print(self.curr_animation_time, self.animation_time)
        if self.previous_state == self.state:
            if self.state != "jumping_left" and self.state != "jumping_right":
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

    def cast(self, deltatime, direction):
        if self.curr_cast_time >= self.cast_time:
            self.curr_cast_time = 0
            if direction == 1:
                projectile_group.add(Projectile(
                    random.choice(projectile_right_images),
                    self.rect.x + self.rect.width - 8,
                    self.rect.y,
                    direction
                ))
            elif direction == -1:
                projectile_group.add(Projectile(
                    random.choice(projectile_left_images),
                    self.rect.x - projectile_left_images[0].get_rect().width,
                    self.rect.y,
                    direction
                ))
        else:
            self.curr_cast_time += deltatime


parachute = Parachute()
parachute_group = pygame.sprite.GroupSingle(parachute)

projectile_group = pygame.sprite.Group()

player = Player(player_images, parachute)
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
    actions = []
    if keys_pressed[K_SPACE]:
        actions.append("jump")
    if keys_pressed[K_a]:
        actions.append("left")
    if keys_pressed[K_d]:
        actions.append("right")
    if keys_pressed[K_m]:
        direction = 1 if "right" in player.state else -1
        player.cast(deltatime, direction)

    player.move(deltatime, actions)

    for p in projectile_group:
        p.move(deltatime)

    # Display update
    # pygame.Surface.fill(window, background_color)
    pygame.Surface.blit(window, background_image, (0, 0))

    projectile_group.draw(window)
    parachute_group.draw(window)
    player_group.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
