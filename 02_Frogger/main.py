import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 1000, 600
FPS = 60
GAME_TITLE = 'Frogger - MarconiGames'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
gamefont = pygame.font.SysFont("monospace", 200)
font_color = (255, 255, 255)

# Game Values

win_label = gamefont.render("You Win!", 1, font_color)
win_rect = win_label.get_rect()
win_label_x = WIDTH // 2 - win_rect.width // 2
win_label_y = HEIGHT // 2 - win_rect.height // 2

lose_label = gamefont.render("You Lose!", 1, font_color)
lose_rect = lose_label.get_rect()
lose_label_x = WIDTH // 2 - lose_rect.width // 2
lose_label_y = HEIGHT // 2 - lose_rect.height // 2

background_color = (100, 210, 60) # RGB value
street_color = (15, 15, 15)

player_sprite = pygame.image.load('./images/player_sprite.png')
player_win_sprite = pygame.image.load('./images/player_win_sprite.png')
player_lose_sprite = pygame.image.load('./images/player_lose_sprite.png')
player_rect = player_sprite.get_rect()
player_x = 400
player_y = 500

enemy_sprite = pygame.image.load('./images/enemy_sprite.png')
enemy_rect = enemy_sprite.get_rect()

difficulty = 2

class Enemy:

    def __init__(self, y):
        if y in [100, 300]:
            self.x = -1*enemy_rect.width + random.randint(-WIDTH // 2, WIDTH // 2)
            self.x_speed = random.randint(2*difficulty, 3*difficulty)
        if y in [200, 400]:
            self.x = WIDTH + random.randint(-WIDTH // 2, WIDTH // 2)
            self.x_speed = random.randint(-3*difficulty, -2*difficulty)
        self.y = y

list_of_enemies = [[Enemy(y) for _ in range(0, difficulty)] for y in [100, 200, 300, 400]]
win = None

# print(list_of_enemies)

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
            if event.key == K_UP and win == None:
                player_y -= 100
            if event.key == K_LEFT and win == None:
                player_x -= 100
            if event.key == K_RIGHT and win == None:
                player_x += 100

    ##### Game logic
    # Keeping player into screen
    if player_x < 0:
        player_x = 0
    if player_x + player_rect.width >= WIDTH:
        player_x = WIDTH - player_rect.width

    # Moving enemies
    for row in list_of_enemies:
        for enemy in row:
            enemy.x += enemy.x_speed

    # Keeping enemies into screen
    for row in list_of_enemies:
        for enemy in row:
            if enemy.x < -enemy_rect.width:
                enemy.x = WIDTH
            elif enemy.x > WIDTH:
                enemy.x = -enemy_rect.width

    # Check if player won the game
    if player_y == 0 and win == None:
        win = True

    # Control if player hits enemies
    for row in list_of_enemies:
        for enemy in row:
            if enemy.x_speed < 0:
                if  enemy.x > player_x and \
                    enemy.x < player_x + player_rect.width and \
                    enemy.y + enemy_rect.height > player_y and \
                    enemy.y < player_y + player_rect.height and \
                    win == None:
                    win = False
            if enemy.x_speed > 0:
                if  enemy.x + enemy_rect.width > player_x and \
                    enemy.x + enemy_rect.height < player_x + player_rect.width and \
                    enemy.y + enemy_rect.height > player_y and \
                    enemy.y < player_y + player_rect.height and \
                    win == None:
                    win = False


    ##### Display rendering
    pygame.Surface.fill(window, background_color)

    # Street Drawing
    pygame.draw.rect(window, street_color, (0, 100, WIDTH, 400))
    for y in [200, 300, 400]:
        for x in range(0, WIDTH, 75):
            pygame.draw.rect(window, (255, 255, 255), (x, y, 30, 2))

    # Enemy Drawing
    for row in list_of_enemies:
        for enemy in row:
            pygame.Surface.blit(window, enemy_sprite, (enemy.x, enemy.y))

    # Frog Drawing
    if win == None:
        pygame.Surface.blit(window, player_sprite, (player_x, player_y))
    if win == True:
        pygame.Surface.blit(window, player_win_sprite, (player_x, player_y))
    if win == False:
        pygame.Surface.blit(window, player_lose_sprite, (player_x, player_y))

    # Win/Lose Label Drawing
    if win == True:
        pygame.Surface.blit(window, win_label, (win_label_x, win_label_y))
    if win == False:
        pygame.Surface.blit(window, lose_label, (lose_label_x, lose_label_y))


    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
