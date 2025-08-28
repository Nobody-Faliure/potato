from __future__ import annotations

from pygame import Surface, Vector2, SRCALPHA

from node import Node
from terrain_node import TerrainNode, DirtNode


class TerrainSegment(Node):
    def __init__(self, pos: Vector2, size: Vector2):
        super().__init__(pos)
        self._size = size
        num_cols = int(size.x // TerrainNode.BLOCK_SIZE.x)
        num_rows = int(size.y // TerrainNode.BLOCK_SIZE.y)
        for j in range(num_rows):
            for i in range(num_cols):
                node_left_top = Vector2(i * TerrainNode.BLOCK_SIZE.x, j * TerrainNode.BLOCK_SIZE.y)
                self.add_child(DirtNode(node_left_top))

    def render(self):
        return Surface(self._size, SRCALPHA)