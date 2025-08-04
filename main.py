import pygame
import sys

from character import Player

from level import Level
from screen_proxy import ScreenProxy
from terrain_builder import TerrainBuilder, DirtAndStoneGroundSegment, Forest

pygame.init()
touching = False

# Screen height, Screen width
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Bool to break from game loop
running = True

# Create Level
level_box = pygame.Rect(0, 0, screen_width, screen_height)
screen_proxy = ScreenProxy(screen, level_box)
builders: list[TerrainBuilder] = [
    DirtAndStoneGroundSegment(level_box, 0, 10, 4, screen_proxy),
    DirtAndStoneGroundSegment(level_box, 11, 10, 7, screen_proxy),
    DirtAndStoneGroundSegment(level_box, 22, 10, 4, screen_proxy),
    Forest(level_box, 0, 5, 10, screen_proxy),
]
level = Level(level_box.h, level_box.w, level_box)
for builder in builders:
    level.add_terrain_objects(builder.get_terrain_objects())


# Create Player
player = Player(320, 120, screen, level, 0.98, 15, screen_proxy)

# Clock
Clock = pygame.time.Clock()

while running:

    # If exit key is pressed set running to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_j]:
        screen_proxy.scroll(-5,0)
    elif pygame.key.get_pressed()[pygame.K_l]:
        screen_proxy.scroll(5, 0)

    screen.fill((135, 206, 235))

    player.move()
    player.draw()
    level.draw()

    pygame.display.flip()

    Clock.tick(60)

pygame.quit()
sys.exit()