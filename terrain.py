from abc import abstractmethod

from base import Drawable, GameObject, Collidable

import pygame

BLOCK_SIZE = 20

class TerrainObject(Drawable, Collidable, GameObject):
    pass

class Dirt(TerrainObject):
    def __init__(self, x: int , y: int, screen: pygame.Surface, _is_grass):
        self._x = x
        self._y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self._screen = screen
        self._image = pygame.image.load("sprites/dirt.png").convert_alpha()
        self._grass_image = pygame.image.load("sprites/grass.png").convert_alpha()
        self._is_grass = _is_grass

    def get_box(self) -> pygame.Rect:
        return self._box

    def draw(self):
        if self._is_grass:
            self._screen.blit(self._grass_image, self._box)
        else:
            self._screen.blit(self._image, self._box)

class Stone(TerrainObject):
    def __init__(self, x: int , y: int, screen: pygame.Surface):
        self._x = x
        self.y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self._screen = screen
        self._image = pygame.image.load("sprites/stone.png").convert_alpha()

    def get_box(self):
        return self._box

    def draw(self):
        self._screen.blit(self._image, self._box)

class Tree(TerrainObject):
    def __init__(self, x: int, y: int, screen: pygame.Surface):
        self._x = x
        self.y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE * 2)
        self._screen = screen
        self._image = pygame.image.load("sprites/tree.png").convert_alpha()

    def get_box(self):
        return self._box

    def draw(self):
        self._screen.blit(self._image, self._box)

