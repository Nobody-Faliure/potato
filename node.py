from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union, NewType


from pygame import Vector2, Surface, Rect, Mask

class Node(ABC):
    def __init__(self, pos: Vector2 = Vector2(0, 0)) -> None:
        super().__init__()
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

    # override this function to do transform for the surface from current Node and all children nodes
    def transform(self, surface: Surface) -> Surface:
        return surface

    # call render for current node and all children nodes, update the surface cache (aka. _surface in each node)
    def invalidate_surface(self) -> None:
        self._surface = None
        current_node = self
        print("Invalidated ", self)
        while current_node._parent is not None:
            current_node = current_node._parent
            self._parent.invalidate_surface()

    def get_surface(self) -> Surface:
        print("Getting Surface of ", self)
        if self._surface is not None:
            return self._surface
        self._surface = self.render()
        for child in self._children:
            self._surface.blit(child.get_surface(), child._pos)
        self._surface = self.transform(self._surface)
        return self._surface.convert_alpha()

