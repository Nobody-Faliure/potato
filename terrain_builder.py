from abc import ABC

import pygame

from screen_proxy import ScreenProxy
from terrain import Dirt, Stone, Tree, Magma, TerrainObject, BLOCK_SIZE

class TerrainBuilder(ABC):
    def get_terrain_objects(self) -> list[TerrainObject]:
        pass

class DirtAndStoneGroundSegment(TerrainBuilder):
    def __init__(self,
                 level_box: pygame.Rect,
                 x_pos_in_blocks: int,
                 width_in_blocks: int,
                 height_in_blocks: int,
                 screen_proxy: ScreenProxy):
        self._level_box = level_box
        self._x_pos_in_blocks = x_pos_in_blocks
        self._width_in_blocks = width_in_blocks
        self._height_in_blocks = height_in_blocks
        self._screen_proxy = screen_proxy
        self._create_terrain_objects()

    def _create_terrain_objects(self):
        self._terrain_objects: list[TerrainObject] = []
        for i in range(self._width_in_blocks):
            # compute x position
            x = (self._x_pos_in_blocks + i) * BLOCK_SIZE
            for j in range(self._height_in_blocks):
                # compute y position
                y = self._level_box.h - BLOCK_SIZE * (1 + j)
                if y < 0:
                    raise Exception("Number of blocks exceed the height of level")
                # create blocks
                if j == self._height_in_blocks - 1:
                    dirt = Dirt(x, y, True, self._screen_proxy)
                    #print("Dirt: ", x, ", ", y, ", ", True)
                    self._terrain_objects.append(dirt)
                elif j == self._height_in_blocks - 2:
                    dirt = Dirt(x, y, False, self._screen_proxy)
                    #print("Dirt: ", x, ", ", y, ", ", False)
                    self._terrain_objects.append(dirt)
                else:
                    stone = Stone(x, y, self._screen_proxy)
                    #print("Stone: ", x, ", ", y, ", ")
                    self._terrain_objects.append(stone)

    def get_terrain_objects(self):
        return self._terrain_objects

class Forest(TerrainBuilder):
    def __init__(self, level_box: pygame.Rect, x_pos_in_blocks: int, y_pos_in_blocks: int, width_in_blocks: int, screen_proxy: ScreenProxy):
        self._level_box = level_box
        self._x_pos_in_blocks = x_pos_in_blocks
        self._y_pos_in_blocks = y_pos_in_blocks
        self._width_in_blocks = width_in_blocks
        self._screen_proxy = screen_proxy
        self._create_terrain_objects()

    def _create_terrain_objects(self):
        self._terrain_objects: list[TerrainObject] = []
        for i in range(self._width_in_blocks):
            x = (self._x_pos_in_blocks + i) * BLOCK_SIZE
            y = self._level_box.h - (self._y_pos_in_blocks + 1) * BLOCK_SIZE
            tree = Tree(x, y, self._screen_proxy)
            self._terrain_objects.append(tree)

    def get_terrain_objects(self):
        return self._terrain_objects

