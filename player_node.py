import pygame
from pygame import Vector2

from node import Node

class PlayerNode(Node):
    def __init__(self):
        super().__init__()
        self._pos = Vector2(100, 100)
        self._size = Vector2(20, 30)
        self._potato_running_left_sprites: list[pygame.Surface] = [pygame.image.load("sprites/potato_left_1.png"),
                                                                   pygame.image.load("sprites/potato_left_2.png"),
                                                                   pygame.image.load("sprites/potato_left_3.png"),
                                                                   pygame.image.load("sprites/potato_left_4.png")]
        self._potato_running_right_sprites: list[pygame.Surface] = [pygame.image.load("sprites/potato_right_1.png"),
                                                                    pygame.image.load("sprites/potato_right_2.png"),
                                                                    pygame.image.load("sprites/potato_right_3.png"),
                                                                    pygame.image.load("sprites/potato_right_4.png")]
        self._potato_standby: pygame.Surface = pygame.image.load("sprites/potato_standby.png").convert_alpha()
        self._velocity: Vector2 = Vector2(0, 0)
        self._max_x_velocity: float = 2
        self._x_acceleration: float = 1
        self._gravity: float = 0.98

    def render(self) -> pygame.Surface:
        print("Player Rendered")
        return self._potato_standby

    def process_movement(self) -> None:
        # process user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self._velocity.x -= self._x_acceleration
            self.invalidate_surface()
        elif keys[pygame.K_RIGHT]:
            self._velocity.x += self._x_acceleration
            self.invalidate_surface()
        else:
            self._velocity.x = 0

        # process velocity
        if self._velocity.x > 2:
            self._velocity.x = 2
        elif self._velocity.x < -2:
            self._velocity.x = -2
        self._pos.x += self._velocity.x


