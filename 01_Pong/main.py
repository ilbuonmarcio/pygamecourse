import pygame
import random
from pygame.locals import *

pygame.init()

GAME_RES = WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TITLE = 'Pong - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
pygame.key.set_repeat(10,10)
clock = pygame.time.Clock()
gamefont = pygame.font.SysFont("monospace", 30)
font_color = (0, 0, 0)

# Game Values

class Player(pygame.sprite.Sprite):

    def __init__(self, image, side='left'):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.y_speed = 10

        self.score = 0
        self.set_side(side)

    def set_side(self, side='left'):
        if side == 'left':
            self.rect.x = 20
            self.rect.y = HEIGHT // 2 - self.rect.height // 2
            self.score_coords = (20, 20)
        if side == 'right':
            self.rect.x = WIDTH - 20 - self.rect.width
            self.rect.y = HEIGHT // 2 - self.rect.height // 2
            self.score_coords = (WIDTH - 50, 20)


class Ball(pygame.sprite.Sprite):

    def __init__(self, image, x_speed=None, y_speed=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        if x_speed == None:
            self.x_speed = random.choice((-5, -4, -3, 3, 4, 5))
        else:
            self.x_speed = x_speed

        if y_speed == None:
            self.y_speed = random.choice((-5, -4, -3, 3, 4, 5))
        else:
            self.y_speed = y_speed

        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

    def reset_ball(self):
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.x_speed = random.choice((-5, -4, -3, 3, 4, 5))
        self.y_speed = random.choice((-5, -4, -3, 3, 4, 5))


player1_image = pygame.image.load('./images/player_sprite.png')
player2_image = pygame.image.load('./images/enemy_sprite.png')
ball_image = pygame.image.load('./images/ball_sprite.png')


player1 = Player(player1_image, 'left')
player2 = Player(player2_image, 'right')
ball = Ball(ball_image)

player_group = pygame.sprite.Group(player1, player2)
ball_group = pygame.sprite.Group(ball)
# ball_group = pygame.sprite.Group([Ball(ball_image) for i in range(0, 1)])


background_color = (200, 200, 200)

# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    ##### Event handling
    for event in pygame.event.get():

        # Handling keys for closing the game
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break

    # Players' Input Handling
    keys_pressed = pygame.key.get_pressed()

    # Player1 Input
    if keys_pressed[K_w]:
        player1.rect.y -= player1.y_speed
    if keys_pressed[K_s]:
        player1.rect.y += player1.y_speed

    # Player2 Input
    if keys_pressed[K_o]:
        player2.rect.y -= player2.y_speed
    if keys_pressed[K_k]:
        player2.rect.y += player2.y_speed

    ##### Game logic
    # Move ball
    for ball in ball_group:
        ball.rect.x += ball.x_speed
        ball.rect.y += ball.y_speed

        # Bouce into bars if collision is made
        if pygame.sprite.spritecollide(ball, player_group, False) != []:
            ball.x_speed *= -1

        # Keeping ball into screen
        if ball.rect.x + ball.rect.width >= WIDTH:
            player1.score += 1
            ball.reset_ball()

        if ball.rect.x <= 0:
            player2.score += 1
            ball.reset_ball()

        if ball.rect.y + ball.rect.height >= HEIGHT or ball.rect.y <= 0:
            ball.y_speed *= -1

    # Keeping bars into screen
    if player1.rect.y + player1.rect.height >= HEIGHT - 20:
        player1.rect.y = HEIGHT - player1.rect.height - 20
    if player1.rect.y < 20:
        player1.rect.y = 20

    if player2.rect.y + player2.rect.height >= HEIGHT - 20:
        player2.rect.y = HEIGHT - player2.rect.height - 20
    if player2.rect.y < 20:
        player2.rect.y = 20

    ##### Display Rendering
    # Score buffer rendering
    player1_score_buffer = gamefont.render(str(player1.score),
                                           1,
                                            font_color)
    player2_score_buffer = gamefont.render(str(player2.score),
                                           1,
                                            font_color)

    # Window reset
    pygame.Surface.fill(window, background_color)

    # Game elements drawing
    player_group.draw(window)
    ball_group.draw(window)

    # UI/UX drawing
    pygame.Surface.blit(window,
                        player1_score_buffer,
                        player1.score_coords)
    pygame.Surface.blit(window,
                        player2_score_buffer,
                        player2.score_coords)

    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
