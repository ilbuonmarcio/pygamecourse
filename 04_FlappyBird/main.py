import pygame
from pygame.locals import *
import random

pygame.init()

GAME_RES = WIDTH, HEIGHT = 1080, 1920
FPS = 60
GAME_TITLE = 'Flappy Bird'

window = pygame.display.set_mode(GAME_RES, HWACCEL|HWSURFACE|DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Game Values

background_image = pygame.image.load("./images/Background.png")


class Ghost:

    player_sprite = pygame.image.load('./images/Ghost.png')
    player_rect = player_sprite.get_rect()
    player_x = WIDTH / 6
    player_y = HEIGHT / 2 - player_rect.height / 2
    speed_up = HEIGHT / 10
    speed_down = 15

    # Set up the bounce of the ghost when mouse is pressed
    def bounce(self):
        for i in range(10):
            self.player_y -= self.speed_up / 10

    # Check if the mouse is pressed
    def isPressed(self):
        if pygame.mouse.get_pressed()[0]:
            return True

    # Check if the ghost is touching a wall or is into the screen
    def isDead(self):
        if self.player_y < 0:
            return True
        if self.player_y > (HEIGHT - self.player_rect.height):
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
wall_sprite_up = pygame.image.load('./images/Wall_up.png')
wall_rect_up = wall_sprite_up.get_rect()
wall_rect_down = wall_sprite_down.get_rect()
list_of_walls_down = []
list_of_walls_up = []
speed_wall = 5

class Walls:
    # Function that creates walls in a random position
    def createWall(self):
        wall_x_down = WIDTH + 100
        wall_x_up = wall_x_down
        wall_y_down = random.randint((HEIGHT / 2), (HEIGHT - 400))
        wall_y_up = wall_y_down - wall_rect_up.height - 700

        down_y, down_x = wall_y_down, wall_x_down
        list_of_walls_down.insert(0, [down_y, down_x])

        up_y, up_x = wall_y_up, wall_x_up
        list_of_walls_up.insert(0, [up_y, up_x])

    # Draw the walls on the screen
    def draw(self):
        for block in list_of_walls_down[::-1]:
            pygame.Surface.blit(window, wall_sprite_down, (block[1], block[0]))
        for block in list_of_walls_up[::-1]:
            pygame.Surface.blit(window, wall_sprite_up, (block[1], block[0]))


wall = Walls()

# Set up the timer for the generation and the elimination of the walls
timer_generation = 0
timer_dead = 0
timer_dead_start = 0

# Delete a wall
def deleteWall():
    if timer_dead_start == 1200:
        if timer_dead == 120:
            timer_dead = 0
            return True
        else:
            timer_dead += 1
    else:
        timer_dead_start += 1



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
        if ghost.isPressed():
            ghost.bounce()
            break

    # Check if the ghost is dead
    if ghost.isDead():
        game_ended = True

    # Game logic
    physics()

    # Fill Background
    window.blit(background_image, [0, 0])

    # Ghost Drawing
    pygame.Surface.blit(window, ghost.player_sprite, (ghost.player_x, \
                                                      ghost.player_y))

    # Walls Drawing
    wall.draw()

    # Wall Moving
    if len(list_of_walls_down) > 0:
        for i in range(len(list_of_walls_down)):
            list_of_walls_down[i][1] -= speed_wall
            list_of_walls_up[i][1] -= speed_wall

    # Wait for wall generation
    if timer_generation == 120:
        wall.createWall()
        timer_generation = 0
    else:
        timer_generation += 1

    # Delete a wall
    if deleteWall():
        del list_of_walls_down[-1]
        del list_of_walls_up[-1]

    # Display Update
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
