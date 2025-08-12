# from abc import ABC

import pygame

from base import Drawable, Collidable, GameObject
from game_session import GameSession
from screen_proxy import ScreenProxy

from enum import Enum
from level import Level

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 30

class Player(Drawable, Collidable, GameObject):
    class State(Enum):
        ON_THE_GROUND = 0
        IN_THE_AIR = 1

    class MovementKeyPressed(Enum):
        NO_KEY = 0
        LEFT_KEY = 1
        RIGHT_KEY = 2

    def __init__(self,
                 screen: pygame.Surface,
                 level: Level,
                 gravity_acceleration: float,
                 jump_initial_velocity: float,
                 screen_proxy : ScreenProxy,
                 game_session : GameSession,
                 speed: int):
        self._state = self.State.IN_THE_AIR
        self._gravity_acceleration = gravity_acceleration
        self._original_x = 320
        self._original_y = 0
        self._box = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
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
        self._game_session = game_session
        self._hp_change_value = 0
        self._death_message = None
        self._movement_key_pressed = self.MovementKeyPressed.NO_KEY
        self._speed = speed

    def process_jumping_and_collision(self) -> None:
        # move horizontal
        self.get_box().move_ip(self._x_velocity, 0)
        if self.has_collision():
            # revert the move
            self.get_box().move_ip(-self._x_velocity, 0)
            # find maximum x delta
            target_x = self.get_box().x + self._x_velocity
            step_x = (self._x_velocity > 0) - (self._x_velocity < 0)
            while self.get_box().x < target_x and step_x != 0:
                self._box.move_ip(step_x, 0)
                if self.has_collision():
                    self._box.move_ip(-step_x, 0)
                    break

        self._movement_key_pressed = self.MovementKeyPressed.NO_KEY

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


    def draw(self) -> None:
        if self._movement_key_pressed == self.MovementKeyPressed.NO_KEY:
            self._x_velocity = 0
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

        self.process_jumping_and_collision()

    def move(self) -> None:
        pass

    def get_box(self) -> pygame.Rect:
        return self._box

    def move_left(self):
        self._left_frame_index = (self._left_frame_index + 1) % 20
        self._x_velocity = self._speed * -1
        self._movement_key_pressed = self.MovementKeyPressed.LEFT_KEY

    def move_right(self):
        self._right_frame_index = (self._right_frame_index + 1) % 20
        self._x_velocity = self._speed
        self._movement_key_pressed = self.MovementKeyPressed.LEFT_KEY

    def jump(self):
        if self._state == Player.State.ON_THE_GROUND:
            self._state = self.State.IN_THE_AIR
            self._y_velocity = self._jump_initial_velocity * -1

    def has_collision(self) -> bool:
        collide_with_terrain = self._level.collide(self)
        collide_with_border = self._box.x <= 0 or self._box.x >= self._level.get_box().width - PLAYER_WIDTH
        return collide_with_border or collide_with_terrain

    def reset(self):
        self._box.x = self._original_x
        self._box.y = self._original_y
        self._x_velocity = 0
        self._y_velocity = 0
        self._state = self.State.IN_THE_AIR
        self._hp_change_value = 0
        self._game_session.change_state(GameSession.GameSessionState.IN_GAME)
        self._screen_proxy.revert()

    def process_hp(self) -> None:
        #void damage
        if self._box.y >= self._level.get_box().height and self._game_session.get_state() == GameSession.GameSessionState.IN_GAME:
            self._death_message = "Potato was yeeted into nonexistence"
            self._hp_change_value = - 100
        if self._box.y < 0 and self._game_session.get_state() == GameSession.GameSessionState.IN_GAME:
            self._death_message = "Potato was yeeted into outer space"
            self._hp_change_value = - 100
        self._game_session.process_hp(self._hp_change_value)
        self._hp_change_value = 0

    def get_death_message(self) -> str:
        return self._death_message
