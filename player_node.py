import pygame
from pygame import Vector2

from node import Node
from animation import Animation

class PlayerNode(Node, Animation):
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
        self._gravity: float = 0.98
        Animation.add_animation(self,
                                "player movement x",
                                0,
                                None,
                                1,
                                False,
                                False,
                                self._pos.x,
                                2)

    def render(self) -> pygame.Surface:
        print("Player Rendered")
        return self._potato_standby

    def process_movement(self) -> None:
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.invalidate_surface()
            self.update_increment("player movement x", -0.2, False)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.invalidate_surface()
            self.update_increment("player movement x", 0.2, False)
        else:
            self.update_increment("player movement x", 0, True)

        self.process_animation("player movement x")
        self._pos.x = self.get_animated_value("player movement x")




