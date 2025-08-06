from __future__ import annotations
from abc import abstractmethod, ABC

import pygame


class GameObject(ABC):
    pass

class Collidable(GameObject):
    @abstractmethod
    def get_box(self) -> pygame.Rect:
        pass

    def collide(self, other: Collidable) -> bool:
        return self.get_box().colliderect(other.get_box())

class Drawable(GameObject):
    @abstractmethod
    def draw(self):
        pass

