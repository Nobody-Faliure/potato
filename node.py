from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union

from pygame import Vector2, Surface, Rect, Mask


class Node(ABC):
    def __init__(self, pos: Vector2) -> None:
        self._surface: Optional[Surface] = None
        self._pos: Vector2 = pos
        self._parent: Optional[Node] = None
        self._children: list[Node] = []
        pass

    def add_child(self, child: Node) -> None:
        child._parent = self
        self._children.append(child)

    # override this function to generate Surface for current Node
    @abstractmethod
    def render(self) -> Surface:
        pass

    # override this function to provide collision shape, relative to local coordination
    @abstractmethod
    def get_collision_shape(self) -> Union[Rect, Mask]:
        pass

    # override this function to do transform for the surface from current Node and all children nodes
    @abstractmethod
    def transform(self, surface: Surface) -> Surface:
        return surface

    # call render for current node and all children nodes, update the surface cache (aka. _surface in each node)
    def invalidate_surface(self) -> None:
        self._surface = self.render()
        for child in self._children:
            child.invalidate_surface()
            child.get_surface().blit(self._surface, child._pos)
        self._surface = self.transform(self._surface)

    def get_surface(self) -> Surface:
        return self._surface

