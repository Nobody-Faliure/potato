from abc import abstractmethod, ABC

import pygame

class GameObject(ABC):
    @abstractmethod
    def getBox(self) -> pygame.Rect:
        pass

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Moveable(ABC):
    @abstractmethod
    def move(self):
        pass