import pygame

from terrain import Dirt, Stone, Tree, BLOCK_SIZE
from level import Level

import random

def build_random_terrain(screen: pygame.Surface):
    level = Level(480, 640, screen)
    for i in range(0, 32):
        number = random.randint(1, 4)
        if number == 4:
            number = random.randint(1, 5)
            if number == 1:
                level.add_terrain_object([Tree(i * BLOCK_SIZE, 340, screen)])
            level.add_terrain_object([
                Dirt(i * BLOCK_SIZE, 380, screen, True),
                Dirt(i * BLOCK_SIZE, 400, screen, False),
                Stone(i * BLOCK_SIZE, 420, screen),
                Stone(i * BLOCK_SIZE, 440, screen)
            ])
        elif number == 3:
            number = random.randint(1, 5)
            if number == 1:
                level.add_terrain_object([Tree(i * BLOCK_SIZE, 360, screen)])
            level.add_terrain_object([
                Dirt(i * BLOCK_SIZE, 400, screen, True),
                Dirt(i * BLOCK_SIZE, 420, screen, False),
                Stone(i * BLOCK_SIZE, 440, screen)
            ])
        elif number == 2:
            number = random.randint(1, 5)
            if number == 1:
                level.add_terrain_object([Tree(i * BLOCK_SIZE, 380, screen)])
            level.add_terrain_object([
                Dirt(i * BLOCK_SIZE, 420, screen, True),
                Stone(i * BLOCK_SIZE, 440, screen)
            ])
        elif number == 1:
            level.add_terrain_object([Dirt(i * BLOCK_SIZE, 440, screen, True)])

    return level