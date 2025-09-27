from __future__ import annotations

import pygame
from pygame import Vector2

from node import Node
from animator import AcceleratedAnimator

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
        ##self._gravitational_animator: AcceleratedAnimator = AcceleratedAnimator(self._pos.y, , 0, 9.8)

    def render(self) -> pygame.Surface:
        print("Player Rendered")
        return self._potato_standby

    def moveTo(self, pos: Vector2) -> None:
        self._pos = pos
        self._parent.invalidate_surface()

    def process_user_input(self) -> None:
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.invalidate_surface()
            self._pos.x -= 2
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.invalidate_surface()
            self._pos.x += 2




