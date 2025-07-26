import pygame

from base import Collidable, Drawable, GameObject
from terrain import TerrainObject, Magma

AREA_SIZE = 100

def _encode_area_key(area_coord_x: int, area_coord_y: int) -> int:
    return area_coord_x * 256 + area_coord_y

class Level(Drawable, GameObject):
    def __init__(self, level_height: float, level_width: float, screen: pygame.Surface, level_box: pygame.Rect):
        self._level_box = level_box
        self._objects_map = dict[int, list[TerrainObject]]()
        self._max_area_coord_x = int((level_width - 1) // AREA_SIZE)
        self._max_area_coord_y = int((level_height - 1) // AREA_SIZE)
        self._screen = screen

    def add_terrain_object(self, terrain_objects: list[TerrainObject]):
        terrain_object_boxes = list(map(lambda x: x.get_box(), terrain_objects))
        # if all terrain objects in level box
        if self._level_box.unionall(terrain_object_boxes) != self._level_box:
            raise Exception("At least one terrain object is out of level bound")
        for terrain_object in terrain_objects:
            # set coordinates for area
            area_coord_x = terrain_object.get_box().x // AREA_SIZE
            area_coord_y = terrain_object.get_box().y // AREA_SIZE
            area_key = _encode_area_key(area_coord_x, area_coord_y)
            # make new are if no area with valid coordinates
            if area_key not in self._objects_map:
                self._objects_map[area_key] = []
            self._objects_map[area_key].append(terrain_object)

    def collide(self, other: Collidable) -> bool:
        center_area_coord_x = other.get_box().x // AREA_SIZE
        center_area_coord_y = other.get_box().y // AREA_SIZE
        for area_coord_x in range(max(center_area_coord_x - 1, 0), min(center_area_coord_x + 1, self._max_area_coord_x) + 1):
            for area_coord_y in range(max(center_area_coord_y - 1, 0), min(center_area_coord_y + 1, self._max_area_coord_y) + 1):
                area_key = _encode_area_key(area_coord_x, area_coord_y)
                if area_key not in self._objects_map:
                    continue
                for terrain_object in self._objects_map[area_key]:
                    if terrain_object.collide(other):
                        return True
        return False

    def draw(self):
        for terrain_objects in self._objects_map.values():
            for terrain_object in terrain_objects:
                terrain_object.draw()

    def get_box(self) -> pygame.Rect:
        return self._level_box

