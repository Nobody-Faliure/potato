from abc import ABC

import pygame

from base import Drawable, Moveable, GameObject
from terrain import TerrainObject

PLAYER_SIZE = 20

class Player(Drawable, Moveable, GameObject):
    def __init__(self, x, y, screen: pygame.Surface, terrain_objects: list[TerrainObject]):
        self._x = x
        self._y = y
        self._box = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self._terrain_objects = terrain_objects
        self._screen = screen

    def draw(self):
        pygame.draw.rect(self._screen,(255, 0, 0), self._box)

    def move(self):
        self.process_user_input()
        self.process_drop_and_collision()

    def getBox(self) -> pygame.Rect:
        return self._box

    def process_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._box.x -= 2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._box.x += 2

    def process_drop_and_collision(self):
        touching = False
        for terrain_object in self._terrain_objects:
            if terrain_object.getBox().colliderect(self._box):
                touching = True
                break

        if not touching:
            self._box.y += 2  # or -= 2 if y=0 is top
