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

# Create Level
level = build_random_terrain(screen)

# Create Player
player = Player(320, 120, screen, level, 1, 15)

# Clock
Clock = pygame.time.Clock()

while running:

    # If exit key is pressed set running to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235))

    player.move()
    player.draw()
    level.draw()

    pygame.display.flip()

    Clock.tick(60)

pygame.quit()
sys.exit()