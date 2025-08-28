from __future__ import annotations

import pygame
from pygame import Vector2, Surface, Rect
import sys

from root_node import RootNode
from terrain_segment_node import TerrainSegment

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))


root_node = RootNode(Vector2(640, 480), Rect(0, 0, 640, 480))

terrain_segment_node = TerrainSegment(Vector2(0, 0), Vector2(20, 20))

root_node.add_child(terrain_segment_node)

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




