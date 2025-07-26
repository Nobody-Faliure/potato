import pygame

from screen_proxy import ScreenProxy
from terrain import Dirt, Stone, Tree, Magma, BLOCK_SIZE
from level import Level

import random

def build_random_terrain(screen: pygame.Surface, screen_proxy : ScreenProxy, level_box: pygame.rect) -> Level:
    level = Level(480, 640 * 4, screen, level_box)
    for i in range(0, 32 * 4):
        number = random.randint(1, 4)
        if number == 4:
            number = random.randint(1, 5)
            if number == 1:
                level.add_terrain_object([Tree(i * BLOCK_SIZE, 340, screen, screen_proxy)])
            level.add_terrain_object([
                Dirt(i * BLOCK_SIZE, 380, screen, True, screen_proxy),
                Dirt(i * BLOCK_SIZE, 400, screen, False, screen_proxy),
                Stone(i * BLOCK_SIZE, 420, screen, screen_proxy),
                Stone(i * BLOCK_SIZE, 440, screen, screen_proxy)
            ])

        elif number == 3:
            number = random.randint(1, 5)
            if number == 1:
                level.add_terrain_object([Tree(i * BLOCK_SIZE, 360, screen, screen_proxy)])
            level.add_terrain_object([
                Dirt(i * BLOCK_SIZE, 400, screen, True, screen_proxy),
                Dirt(i * BLOCK_SIZE, 420, screen, False, screen_proxy),
                Stone(i * BLOCK_SIZE, 440, screen, screen_proxy)
            ])
        elif number == 2:
            number = random.randint(1, 5)
            if number == 1:
                level.add_terrain_object([Tree(i * BLOCK_SIZE, 380, screen, screen_proxy)])
            level.add_terrain_object([
                Dirt(i * BLOCK_SIZE, 420, screen, True, screen_proxy),
                Stone(i * BLOCK_SIZE, 440, screen, screen_proxy)
            ])
        elif number == 1:
            number = random.randint(1, 3)
            if number == 1:
                level.add_terrain_object([Magma(i * BLOCK_SIZE, 440, screen, screen_proxy)])
            else:
                level.add_terrain_object([Dirt(i * BLOCK_SIZE, 440, screen, True, screen_proxy)])

    return level