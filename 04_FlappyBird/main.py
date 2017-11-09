import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 1000, 640 # 360, 640
FPS = 60
GAME_TITLE = 'Flappy Bird'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_image = pygame.image.load("./images/Background.png")
background_image = pygame.transform.scale(background_image,
                                       (background_image.get_rect().width // 2,
                                        background_image.get_rect().height // 2))
background_rect = background_image.get_rect()
background_delta = 0


class Ghost:

    player_sprite = pygame.image.load('./images/Ghost.png')
    player_sprite = pygame.transform.scale(player_sprite,
                                           (int(player_sprite.get_rect().width * 1.5),
                                            int(player_sprite.get_rect().height * 1.5)))
    player_rect = player_sprite.get_rect()
    player_x = WIDTH / 6
    player_y = HEIGHT / 2 - player_rect.height / 2
    speed_up = HEIGHT / 15
    speed_down = 3

    # Set up the bounce of the ghost when mouse is pressed
    def bounce(self):
        self.player_y -= self.speed_up

    # Check if the ghost is touching a wall or is into the screen
    def isDead(self):
        if self.player_y < 0 or \
           self.player_y > HEIGHT - self.player_rect.height:
            return True

        if len(list_of_walls_down) != 0:
            for i in range(len(list_of_walls_down)):
                if (self.player_y > (list_of_walls_down[i][0] - \
                    self.player_rect.height) or self.player_y < \
                    (list_of_walls_up[i][0] + wall_rect_up.height)) \
                    and (self.player_x > (list_of_walls_down[i][1] - \
                    self.player_rect.width) \
                    and self.player_x < list_of_walls_down[i][1]):
                    return True

ghost = Ghost()

# Set up the physics of the ghost
def physics():
    ghost.player_y += ghost.speed_down


# Set up the elementary values of the walls
wall_sprite_down = pygame.image.load('./images/Wall.png')
wall_sprite_down = pygame.transform.scale(wall_sprite_down,
                                          (wall_sprite_down.get_rect().width // 2,
                                           wall_sprite_down.get_rect().height // 2))
wall_sprite_up = pygame.image.load('./images/Wall_up.png')
wall_sprite_up = pygame.transform.scale(wall_sprite_up,
                                          (wall_sprite_up.get_rect().width // 2,
                                           wall_sprite_up.get_rect().height // 2))
wall_rect_up = wall_sprite_up.get_rect()
wall_rect_down = wall_sprite_down.get_rect()
list_of_walls_down = []
list_of_walls_up = []
speed_wall = 7

class Walls:
    # Function that creates walls in a random position
    def createWall(self):
        wall_x_down = WIDTH
        wall_x_up = wall_x_down
        wall_y_down = random.randint((HEIGHT // 1.8), (HEIGHT // 1.2))
        wall_y_up = wall_y_down - wall_rect_up.height - wall_rect_up.height // 2

        down_y, down_x = wall_y_down, wall_x_down
        list_of_walls_down.append([down_y, down_x])

        up_y, up_x = wall_y_up, wall_x_up
        list_of_walls_up.append([up_y, up_x])

    # Draw the walls on the screen
    def draw(self):
        for block in list_of_walls_down:
            pygame.Surface.blit(window, wall_sprite_down, (block[1], block[0]))
        for block in list_of_walls_up:
            pygame.Surface.blit(window, wall_sprite_up, (block[1], block[0]))


wall = Walls()

# Set up the timer for the generation and the elimination of the walls
timer_generation = 0
timer_dead = 0
timer_dead_start = 0


# End of Game Values

# Game loop
game_ended = False
while not game_ended:

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended  = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended  = True
                break
            if event.key == K_UP:
                ghost.bounce()

    ##### Game logic
    physics()

    # Wait for wall generation
    if timer_generation == 60:
        wall.createWall()
        timer_generation = 0
    else:
        timer_generation += 1

    # Delete a wall
    if timer_dead_start == 1200:
        if timer_dead == 120:
            timer_dead = 0
            del list_of_walls_down[-1]
            del list_of_walls_up[-1]
        else:
            timer_dead += 1
    else:
        timer_dead_start += 1

    # Wall Moving
    if len(list_of_walls_down) > 0:
        for i in range(len(list_of_walls_down)):
            list_of_walls_down[i][1] -= speed_wall
            list_of_walls_up[i][1] -= speed_wall

    # Check if the ghost is dead
    if ghost.isDead():
        game_ended = True

    # Fill Background
    for x in range(-background_delta, WIDTH, background_rect.width):
        window.blit(background_image, [x, 0])
    background_delta += 1

    # Ghost Drawing
    pygame.Surface.blit(window, ghost.player_sprite, (ghost.player_x, \
                                                      ghost.player_y))

    # Walls Drawing
    wall.draw()

    ##### Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
