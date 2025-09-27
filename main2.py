from __future__ import annotations

import pygame
from pygame import Vector2, Surface, Rect
import sys

from animator import AcceleratedAnimator
from root_node import RootNode
from terrain_segment_node import TerrainSegment
from player_node import PlayerNode

pygame.init()
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

root_node = RootNode(Vector2(640, 480), Rect(0, 0, 640, 480))
terrain_segment_node = TerrainSegment(Vector2(0, 0), Vector2(20, 20))
player_node = PlayerNode()
root_node.add_child(terrain_segment_node)
root_node.add_child(player_node)

def update_player_position(pos: Vector2) -> bool:
    player_node.moveTo(pos)
    return True

drop_animator = AcceleratedAnimator(
    anim_var_init_val=Vector2(100, 0),
    anim_var_init_velocity=Vector2(0, 0),
    anim_var_acceleration=Vector2(0, 0.9),
    anim_var_update_fn=update_player_position)


# main loop

clock = pygame.time.Clock()
running = True

while running:
    # process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # process animation
    drop_animator.step()

    # update frame
    screen.fill((135, 206, 235))
    viewport = root_node.get_viewport_surface()
    screen.blit(viewport, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()




