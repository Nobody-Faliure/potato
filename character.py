# from abc import ABC

import pygame

from base import Drawable, Moveable, Collidable, GameObject
from terrain import TerrainObject

from enum import Enum

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 30

class Player(Drawable, Moveable, GameObject, Collidable):
    class State(Enum):
        ON_THE_GROUND = 0
        IN_THE_AIR = 1

    def __init__(self,
                 x: float,
                 y: float,
                 screen: pygame.Surface,
                 terrain_objects: list[TerrainObject],
                 gravity_acceleration: float,
                 jump_initial_velocity: float):
        self._state = self.State.IN_THE_AIR
        self._gravity_acceleration = gravity_acceleration
        self._box = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self._terrain_objects = terrain_objects
        self._screen = screen
        self._jump_initial_velocity = jump_initial_velocity
        self._x_velocity = 0
        self._y_velocity = 0
        self._standby_image = pygame.image.load("sprites/potato_standby.png").convert_alpha(screen)
        self._jumping_image = pygame.image.load("sprites/potato_jumping.png").convert_alpha(screen)
        self._left_frames = [
            pygame.image.load("sprites/potato_left_1.png").convert_alpha(screen),
            pygame.image.load("sprites/potato_left_2.png").convert_alpha(screen),
            pygame.image.load("sprites/potato_left_2.png").convert_alpha(screen),
            pygame.image.load("sprites/potato_left_4.png").convert_alpha(screen)]
        self._right_frames = [
            pygame.image.load("sprites/potato_right_1.png").convert_alpha(screen),
            pygame.image.load("sprites/potato_right_2.png").convert_alpha(screen),
            pygame.image.load("sprites/potato_right_3.png").convert_alpha(screen),
            pygame.image.load("sprites/potato_right_4.png").convert_alpha(screen)
        ]
        self._left_frame_index = 0
        self._right_frame_index = 0


    def draw(self):
        if self._x_velocity < 0:
            self._screen.blit(
                self._left_frames[self._left_frame_index // 5],
                (self._box.x - 8, self._box.y + 2)
            )
        elif self._x_velocity > 0:
            self._screen.blit(
                self._right_frames[self._right_frame_index // 5],
                (self._box.x - 8, self._box.y + 2)
            )
        else:
            self._screen.blit(
                self._standby_image,
                (self._box.x - 8, self._box.y + 2)
            )

    def move(self):
        self.process_jumping_and_collision()
        self.process_user_input()

    def get_box(self) -> pygame.Rect:
        return self._box

    def process_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._left_frame_index = (self._left_frame_index + 1) % 20
            self._x_velocity = -2
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._right_frame_index = (self._right_frame_index + 1) % 20
            self._x_velocity = + 2
        else:
            self._x_velocity = 0
        if keys[pygame.K_SPACE] and self._state == self.State.ON_THE_GROUND:
            self._state = self.State.IN_THE_AIR
            self._y_velocity = self._jump_initial_velocity * -1

    def collide_with_any_terrain_object(self):
        for terrain_object in self._terrain_objects:
            if self.collide(terrain_object):
                return True
        return False

    def process_jumping_and_collision(self):
        # move horizontal
        self.get_box().move_ip(self._x_velocity, 0)
        if self.collide_with_any_terrain_object():
            # revert the move
            self.get_box().move_ip(-self._x_velocity, 0)
            # find maximum x delta
            target_x = self.get_box().x + self._x_velocity
            step_x = (self._x_velocity > 0) - (self._x_velocity < 0)
            while self.get_box().x < target_x and step_x != 0:
                self._box.move_ip(0, step_x)
                if self.collide_with_any_terrain_object():
                    self._box.move_ip(0, -step_x)
                    break

        # move vertically
        if self._state == self.State.IN_THE_AIR:
            self._y_velocity += self._gravity_acceleration
        self.get_box().move_ip(0, self._y_velocity)
        if self.collide_with_any_terrain_object():
            self._state = self.State.ON_THE_GROUND
            # revert the move
            self.get_box().move_ip(0, -self._y_velocity)
            # find maximum y delta
            target_y = self.get_box().y + self._y_velocity
            step_y = (self._y_velocity > 0) - (self._y_velocity < 0)
            while self._box.y < target_y and step_y != 0:
                self._box.move_ip(0, step_y)
                if self.collide_with_any_terrain_object():
                    self._box.move_ip(0, -step_y)
                    if step_y > 0:
                        self._y_velocity = self._gravity_acceleration
                    break
        else:
            self._state = self.State.IN_THE_AIR