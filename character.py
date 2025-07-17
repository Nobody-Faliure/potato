# from abc import ABC

import pygame

from base import Drawable, Moveable, GameObject
from terrain import TerrainObject

from enum import Enum

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 30


class Player(Drawable, Moveable, GameObject):
    class State(Enum):
        ON_GROUND = 0
        JUMPING = 1

    def __init__(self, x, y, screen: pygame.Surface, terrain_objects: list[TerrainObject], gravity, jump, jumping):
        self._x = x
        self._y = y
        self._box = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self._terrain_objects = terrain_objects
        self._screen = screen
        self._jump = jump
        self._y_velocity = gravity
        self._jumping = jumping
        self._last_box = None
        self._standby_image = pygame.image.load("sprites/potato_standby.png").convert_alpha(screen)
        self._jumping_image = pygame.image.load("sprites/potato_jumping.png").convert_alpha(screen)
        self._left_frames = [pygame.image.load("sprites/potato_left_1.png").convert_alpha(screen), pygame.image.load("sprites/potato_left_2.png").convert_alpha(screen), pygame.image.load("sprites/potato_left_2.png").convert_alpha(screen), pygame.image.load("sprites/potato_left_4.png").convert_alpha(screen)]
        self._right_frames = [pygame.image.load("sprites/potato_right_1.png").convert_alpha(screen), pygame.image.load("sprites/potato_right_2.png").convert_alpha(screen), pygame.image.load("sprites/potato_right_3.png").convert_alpha(screen), pygame.image.load("sprites/potato_right_4.png").convert_alpha(screen)]
        self._left = 1
        self._right = 1
        self._on_ground = False
        self._x_velocity = 0

    def draw(self):
        if self._x_velocity < 0:
            self._screen.blit(self._left_frames[self._left//5], (self._box.x - 8, self._box.y + 2))
        elif self._x_velocity > 0:
            self._screen.blit(self._right_frames[self._right//5], (self._box.x - 8, self._box.y + 2))
        else:
            self._screen.blit(self._standby_image, (self._box.x - 8, self._box.y + 2))


    def move(self):
        self.process_jumping_and_collision()
        self.process_user_input()

    def getBox(self) -> pygame.Rect:
        return self._box

    def process_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._left += 1
            if self._left >= 20:
                self._left = 1
            self._x_velocity = -2
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._right += 1
            if self._right >= 20:
                self._right = 1
            self._x_velocity = + 2
        elif keys[pygame.K_SPACE] and self._jumping == False:
            self._jumping = True
            self._on_ground = False
            self._y_velocity = self._jump * -1
            self._box.y -= self._jump
        else:
            self._x_velocity = 0

    def process_jumping_and_collision(self):
        #Save previous position
        self._last_box = self._box.copy()

        #Move horizontally
        self._box.x += self._x_velocity

        #Horizontall collision check
        for terrain_object in self._terrain_objects:
            if terrain_object.getBox().left < self._box.right and terrain_object.getBox().right > self._box.left and terrain_object.getBox().top < self._box.bottom:
                if self._x_velocity > 0:
                    self._box.right = terrain_object.getBox().left
                elif self._x_velocity < 0:
                    self._box.left = terrain_object.getBox().right
                self._x_velocity = 0
                break

        self._box.y += self._y_velocity

        self._on_ground = False

        for terrain_object in self._terrain_objects:
            if terrain_object.getBox().colliderect(self._box):
                if self._y_velocity > 0:
                    self._box.bottom = terrain_object.getBox().top
                    self._on_ground = True
                    self._jumping = False
                    self._y_velocity = 0
                    self._jump = 15
                elif self._y_velocity < 0:
                    self._box.top = terrain_object.getBox().bottom
                    self._y_velocity = 0
                break

        if not self._on_ground:
            self._y_velocity += 1

        if self._jumping and self._on_ground:
            self._y_velocity -= self._jump
            self._on_ground = False