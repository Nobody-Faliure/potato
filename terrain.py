#from abc import abstractmethod

from base import Drawable, GameObject, Collidable

import pygame

from screen_proxy import ScreenProxy

BLOCK_SIZE = 20

class TerrainObject(Drawable, Collidable, GameObject):
    pass

class Dirt(TerrainObject):
    def __init__(self, x: float, y: float, has_grass: bool, screen_proxy: ScreenProxy):
        self._x = x
        self._y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self._image = pygame.image.load("sprites/dirt.png").convert_alpha()
        self._grass_image = pygame.image.load("sprites/grass.png").convert_alpha()
        self._has_grass = has_grass
        self._screen_proxy = screen_proxy

    def get_box(self) -> pygame.Rect:
        return self._box

    def draw(self):
        if self._has_grass:
            self._screen_proxy.blit(self._grass_image, self._box.x, self._box.y)
        else:
            self._screen_proxy.blit(self._image, self._box.x, self._box.y)

class Stone(TerrainObject):
    def __init__(self, x: float , y: float, screen_proxy: ScreenProxy):
        self._x = x
        self.y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self._image = pygame.image.load("sprites/stone.png").convert_alpha()
        self._screen_proxy = screen_proxy

    def get_box(self):
        return self._box

    def draw(self):
        self._screen_proxy.blit(self._image, self._box.x, self._box.y)

class Tree(TerrainObject):
    def __init__(self, x: float, y: float, screen_proxy: ScreenProxy):
        self._x = x
        self.y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE * 2)
        self._image = pygame.image.load("sprites/tree.png").convert_alpha()
        self._screen_proxy = screen_proxy

    def get_box(self):
        return self._box

    def draw(self):
        self._screen_proxy.blit(self._image, self._box.x, self._box.y)

class Magma(TerrainObject):
    def __init__(self, x: float, y: float, screen_proxy: ScreenProxy):
        self._x = x
        self.y = y
        self._box = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self._image = pygame.image.load("sprites/magma.png").convert_alpha()
        self._screen_proxy = screen_proxy

    def get_box(self):
        return self._box

    def draw(self):
        self._screen_proxy.blit(self._image, self._box.x, self._box.y)