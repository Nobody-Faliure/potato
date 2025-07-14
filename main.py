import pygame
import sys

from character import Player
from terrain import Dirt

from base import Drawable, Moveable, GameObject

pygame.init()

# Screen height, Screen width
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")

# Bool to break from game loop
running = True

# Make a list of objects
terrain_objects = []
for i in range(0, 63):
    terrain_objects.append(Dirt(i * 20, 460, screen))
    terrain_objects.append(Dirt(i * 20, 440, screen))
player = Player(320, 240, screen, terrain_objects)
objects = terrain_objects + [player]


# Clock
Clock = pygame.time.Clock()

while running:

    # If exit key is pressed set running to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235))

    # process movables
    movables = list(filter(lambda obj: isinstance(obj, Moveable), objects))
    for movable in movables:
        movable.move()

    # process drawables
    drawables = list(filter(lambda obj: isinstance(obj, Drawable), objects))
    for drawable in drawables:
        drawable.draw()





    # player and block should have common base class
    # class Drawable: draw
    # class Movable: move, collide
    # class Collidable: getHitBox
    # class Character(Drawable, Movable)
    # class Dirt(Drawable)

    # put all sprite in single array sprites
    #
    # collidables = filter(lambda x: issubclass(sprite, Collidable), sprites)
    # in main loop do
    # for sprite in sprites:
    #     process collide
    #     if issubclass(sprite, Movable):
    #         sprite.collide(collidables)
    #         sprite.move()
    #     process moves
    #     if issubclass(sprite, Drawable):
    #          sprite.draw()

    #     if issubclass(sprite, Drawable):
    #          sprite.draw()

    # for movable in movables:
    #   movable.collide(
    #   movable.move

    pygame.display.flip()

    Clock.tick(60)

pygame.quit()
sys.exit()