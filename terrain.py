from abc import abstractmethod

from base import Drawable, GameObject
import pygame

DIRT_SIZE = 20

class TerrainObject(GameObject):
    @abstractmethod
    def getBox(self) -> pygame.Rect:
        pass

class Dirt(Drawable, TerrainObject):
    def __init__(self, x: int , y: int, screen: pygame.Surface):
        self._x = x
        self._y = y
        self._box = pygame.Rect(x, y, DIRT_SIZE, DIRT_SIZE)
        self._screen = screen

    def getBox(self) -> pygame.Rect:
        return self._box

    def draw(self):
        pygame.draw.rect(self._screen, (100, 50, 50), self._box)
