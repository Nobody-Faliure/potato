import pygame
import sys

from character import Player
from terrain_builder import build_random_terrain

from base import Drawable, Moveable, GameObject

pygame.init()
touching = False

# Screen height, Screen width
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Bool to break from game loop
running = True

# Make a list of objects
terrain_objects = build_random_terrain(screen)

player = Player(320, 120, screen, terrain_objects, 1, 15)
objects = terrain_objects + [player]

# Clock
Clock = pygame.time.Clock()

while running:

    # If exit key is pressed set running to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235))

    # process movables
    movables = list(filter(lambda obj: isinstance(obj, Moveable), objects))
    for movable in movables:
        movable.move()

    # process drawables
    drawables = list(filter(lambda obj: isinstance(obj, Drawable), objects))
    for drawable in drawables:
        drawable.draw()

    pygame.display.flip()

    Clock.tick(60)

pygame.quit()
sys.exit()