import pygame

from terrain import Dirt, Stone, Tree, BLOCK_SIZE

import random

def build_random_terrain(screen: pygame.Surface):
    terrain_objects = []
    for i in range(0, 63):
        number = random.randint(1, 4)
        if number == 4:
            number = random.randint(1, 5)
            if number == 1:
                terrain_objects.append(Tree(i * BLOCK_SIZE, 340, screen))
            terrain_objects.append(Dirt(i * BLOCK_SIZE, 380, screen, True))
            terrain_objects.append(Dirt(i * BLOCK_SIZE, 400, screen, False))
            terrain_objects.append(Stone(i * BLOCK_SIZE, 420, screen))
            terrain_objects.append(Stone(i * BLOCK_SIZE, 440, screen))
        elif number == 3:
            number = random.randint(1, 5)
            if number == 1:
                terrain_objects.append(Tree(i * BLOCK_SIZE, 360, screen))
            terrain_objects.append(Dirt(i * BLOCK_SIZE, 400, screen, True))
            terrain_objects.append(Dirt(i * BLOCK_SIZE, 420, screen, False))
            terrain_objects.append(Stone(i * BLOCK_SIZE, 440, screen))
        elif number == 2:
            number = random.randint(1, 5)
            if number == 1:
                terrain_objects.append(Tree(i * BLOCK_SIZE, 380, screen))
            terrain_objects.append(Dirt(i * BLOCK_SIZE, 420, screen, True))
            terrain_objects.append(Stone(i * BLOCK_SIZE, 440, screen))
        elif number == 1:
            terrain_objects.append(Dirt(i * BLOCK_SIZE, 440, screen, True))

    return terrain_objects