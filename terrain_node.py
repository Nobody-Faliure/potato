from __future__ import annotations

from node import Node
from pygame import Surface, Vector2
import pygame

class TerrainNode(Node):

    _image_surface_cache: dict[str, Surface] = {}

    BLOCK_SIZE: Vector2 = Vector2(20, 20)

    def __init__(self, pos: Vector2, image_file: str):
        super().__init__(pos)
        self._image_file: str = image_file

    def render(self) -> Surface:
        if not self._image_file in TerrainNode._image_surface_cache:
            image_surface = pygame.image.load(self._image_file).convert_alpha()
            # assert image_surface == BLOCK_SIZE
            TerrainNode._image_surface_cache[self._image_file] = image_surface
        return TerrainNode._image_surface_cache[self._image_file]

class DirtNode(TerrainNode):
    def __init__(self, pos: Vector2):
        super().__init__(pos, "sprites/dirt.png")

class GrassNode(TerrainNode):
    def __init__(self, pos: Vector2):
        super().__init__(pos, "sprites/grass.png")

class StoneNode(TerrainNode):
    def __init__(self, pos: Vector2):
        super().__init__(pos, "sprites/stone.png")

class MagmaNode(TerrainNode):
    def __init__(self, pos: Vector2):
        super().__init__(pos, "sprites/magma.png")