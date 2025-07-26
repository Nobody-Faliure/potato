# from abc import ABC

import pygame

from base import Drawable, Moveable, Collidable, GameObject
from screen_proxy import ScreenProxy

from enum import Enum
from level import Level

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 30

class Player(Drawable, Moveable, Collidable, GameObject):
    class State(Enum):
        ON_THE_GROUND = 0
        IN_THE_AIR = 1

    def __init__(self,
                 x: float,
                 y: float,
                 screen: pygame.Surface,
                 level: Level,
                 gravity_acceleration: float,
                 jump_initial_velocity: float,
                 screen_proxy : ScreenProxy):
        self._state = self.State.IN_THE_AIR
        self._gravity_acceleration = gravity_acceleration
        self._box = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self._level = level
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
        self._screen_proxy = screen_proxy


    def draw(self) -> None:
        if self._x_velocity < 0:
            self._screen_proxy.blit(
                self._left_frames[self._left_frame_index // 5],
                self._box.x - 8, self._box.y + 2
            )
        elif self._x_velocity > 0:
            self._screen_proxy.blit(
                self._right_frames[self._right_frame_index // 5],
                self._box.x - 8, self._box.y + 2
            )
        else:
            self._screen_proxy.blit(
                self._standby_image,
                self._box.x - 8, self._box.y + 2
            )

    def move(self) -> None:
        self.process_jumping_and_collision()
        self.process_user_input()

    def get_box(self) -> pygame.Rect:
        return self._box

    def process_user_input(self) -> None:
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

    def process_jumping_and_collision(self) -> None:
        # move horizontal
        self.get_box().move_ip(self._x_velocity, 0)
        if self._level.collide(self):
            # revert the move
            self.get_box().move_ip(-self._x_velocity, 0)
            # find maximum x delta
            target_x = self.get_box().x + self._x_velocity
            step_x = (self._x_velocity > 0) - (self._x_velocity < 0)
            while self.get_box().x < target_x and step_x != 0:
                self._box.move_ip(0, step_x)
                if self._level.collide(self):
                    self._box.move_ip(0, -step_x)
                    break

        # move vertically
        if self._state == self.State.IN_THE_AIR:
            self._y_velocity += self._gravity_acceleration
        self.get_box().move_ip(0, self._y_velocity)
        if self._level.collide(self):
            self._state = self.State.ON_THE_GROUND
            # revert the move
            self.get_box().move_ip(0, -self._y_velocity)
            # find maximum y delta
            target_y = self.get_box().y + self._y_velocity
            step_y = (self._y_velocity > 0) - (self._y_velocity < 0)
            while self._box.y < target_y and step_y != 0:
                self._box.move_ip(0, step_y)
                if self._level.collide(self):
                    self._box.move_ip(0, -step_y)
                    if step_y > 0:
                        self._y_velocity = self._gravity_acceleration
                    break
        else:
            self._state = self.State.IN_THE_AIR