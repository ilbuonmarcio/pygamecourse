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

difficulty = 1
win = None

background_color = (100, 210, 60) # RGB value
street_color = (15, 15, 15)

player_images = {
    'alive' : pygame.image.load('./images/player_sprite.png'),
    'win'   : pygame.image.load('./images/player_win_sprite.png'),
    'lose'  : pygame.image.load('./images/player_lose_sprite.png')
}

enemy_image = pygame.image.load('./images/enemy_sprite.png')

vignette_image = pygame.image.load('./images/vignette.png')
vignette_image = pygame.transform.scale(
    vignette_image,
    (WIDTH, HEIGHT)
)

class Player(pygame.sprite.Sprite):

    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images['alive']
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def set_current_sprite(self, key):
        self.image = self.images[key]

class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, direction=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-self.rect.width, WIDTH)
        self.rect.y = random.choice([100, 200, 300, 400])

        self.x_speed = direction * difficulty * random.randint(2, 3)

class Label(pygame.sprite.Sprite):

    def __init__(self, font, string):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(string, 1, font_color)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2

player = Player(player_images)
enemies = [Enemy(enemy_image, random.choice([-1, 1]))
           for _ in range(0, difficulty*2)]
win_label = Label(gamefont, "You Win!")
lose_label = Label(gamefont, "You Lose!")

player_group = pygame.sprite.GroupSingle(player)
enemy_group = pygame.sprite.Group(*enemies)
win_label_group = pygame.sprite.GroupSingle(win_label)
lose_label_group = pygame.sprite.GroupSingle(lose_label)

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
                player.rect.y -= 100
            if event.key == K_LEFT and win == None:
                player.rect.x -= 100
            if event.key == K_RIGHT and win == None:
                player.rect.x += 100
            if event.key == K_SPACE and win == True:
                # Increasing Difficulty
                win = None
                player.rect.x = 400
                player.rect.y = 500
                difficulty += 1
                enemies = [Enemy(enemy_image, random.choice([-1, 1]))
                           for _ in range(0, difficulty*2)]
                enemy_group = pygame.sprite.Group(*enemies)

    ##### Game logic
    # Keeping player into screen
    if player.rect.x < 0:
        player.rect.x = 0
    if player.rect.x + player.rect.width >= WIDTH:
        player.rect.x = WIDTH - player.rect.width

    # Moving enemies
    for enemy in enemies:
        enemy.rect.x += enemy.x_speed

    # Keeping enemies into screen
    for enemy in enemies:
        if enemy.rect.x < -enemy.rect.width:
            enemy.rect.x = WIDTH
        elif enemy.rect.x > WIDTH:
            enemy.rect.x = -enemy.rect.width

    # Check if player won the game
    if player.rect.y == 0 and win == None:
        win = True

    # Control if player hits enemies
    for enemy in enemies:
        if pygame.sprite.spritecollide(player, enemy_group, False) != []:
            win = False

    ##### Display rendering
    pygame.Surface.fill(window, background_color)

    # Street Drawing
    pygame.draw.rect(window, street_color, (0, 100, WIDTH, 400))
    for y in [200, 300, 400]:
        for x in range(0, WIDTH, 75):
            pygame.draw.rect(window, (255, 255, 255), (x, y, 30, 2))

    # Frog Image Swapping
    if win == None:
        player.set_current_sprite('alive')
    if win == True:
        player.set_current_sprite('win')
    if win == False:
        player.set_current_sprite('lose')

    # Player Drawing
    player_group.draw(window)

    # Enemy Drawing
    enemy_group.draw(window)

    pygame.Surface.blit(window, vignette_image, (0, 0))
    
    # Win/Lose Label Drawing
    if win == True:
        win_label_group.draw(window)
    if win == False:
        lose_label_group.draw(window)


    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
