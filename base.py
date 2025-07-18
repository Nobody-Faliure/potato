from __future__ import annotations
from abc import abstractmethod, ABC

import pygame

class GameObject(ABC):
    pass

class Collidable(ABC):
    def collide(self, other: Collidable) -> bool:
        return self.get_box().colliderect(other.get_box())

    @abstractmethod
    def get_box(self) -> pygame.Rect:
        pass

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Moveable(ABC):
    @abstractmethod
    def move(self):
        pass