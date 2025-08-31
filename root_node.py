from __future__ import annotations

from typing import Optional

from pygame import Vector2, Surface, Rect, SRCALPHA
from node import Node

# the root node of rendering tree
# support viewport clipping and scrolling

class RootNode(Node):
    def __init__(self, size: Vector2, viewport_rect: Rect) -> None:
        super().__init__()
        self._size: Vector2 = size
        self._viewport_rect: Rect = viewport_rect
        self._viewport: Optional[Surface] = None

    def render(self) -> Surface:
        print("Root rendered")
        return Surface(self._size, SRCALPHA)

    # viewport related functions
    def invalidate_viewport(self) -> None:
        self._viewport = None

    def scroll_by(self, offset: Vector2) -> bool:
        new_viewport_rect = self._viewport_rect.move(offset)
        if not self._surface.get_rect().contains(new_viewport_rect):
            return False
        self._viewport_rect = new_viewport_rect
        self.invalidate_viewport()
        return True

    def get_viewport_surface(self) -> Surface:
        if self._viewport is not None and self._surface is not None:
            return self._viewport
        self._viewport = self.get_surface().subsurface(self._viewport_rect).convert_alpha()
        return self._viewport










