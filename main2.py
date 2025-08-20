from __future__ import annotations

import pygame
from pygame import Vector2, Surface, Rect
import sys

from node import Node
from root_node import RootNode


class TerrainNode(Node):

    _image_surface_cache: dict[str, Surface] = {}

    def __init__(self, pos: Vector2, image_file: str):
        super().__init__(pos)
        self._image_file: str = image_file

    def render(self) -> Surface:
        if not self._image_file in TerrainNode._image_surface_cache:
            image_surface = pygame.image.load(self._image_file).convert_alpha()
            TerrainNode._image_surface_cache[self._image_file] = image_surface
        return TerrainNode._image_surface_cache[self._image_file]

    def get_collision_shape(self) -> super().CollisionShape:
        return None

    def transform(self, surface: Surface) -> Surface:
        return surface

class DirtNode(TerrainNode):
    def __init__(self, pos: Vector2):
        super().__init__(pos, "sprites/dirt.png")


pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))


root_node = RootNode(Vector2(640, 480), Rect(0, 0, 640, 480))
root_node.add_child(DirtNode(Vector2(0, 0)))

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235))
    viewport = root_node.get_viewport_surface()
    screen.blit(viewport, (0, 0))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()




