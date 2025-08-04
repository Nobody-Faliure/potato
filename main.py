import pygame
import sys

from character import Player
from game_session import GameSession

from level import Level
from screen_proxy import ScreenProxy
from terrain_builder import TerrainBuilder, DirtAndStoneGroundSegment, Forest

pygame.init()
touching = False

# Screen height, Screen width
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Bool to break from game loop
running = True

# Create Level
level_box = pygame.Rect(0, 0, screen_width, screen_height)
screen_proxy = ScreenProxy(screen, level_box)
builders: list[TerrainBuilder] = [
    DirtAndStoneGroundSegment(level_box, 0, 10, 4, screen_proxy),
    DirtAndStoneGroundSegment(level_box, 11, 10, 7, screen_proxy),
    DirtAndStoneGroundSegment(level_box, 22, 10, 4, screen_proxy),
    Forest(level_box, 0, 5, 10, screen_proxy),
]
level = Level(level_box.h, level_box.w, level_box)
for builder in builders:
    level.add_terrain_objects(builder.get_terrain_objects())


# Create Player
game_session = GameSession()
player = Player(screen, level, 0.98, 15, screen_proxy, game_session)

# Clock
Clock = pygame.time.Clock()

while running:
    # If exit key is pressed set running to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_session.get_state() == GameSession.GameSessionState.IN_GAME:
        print("in game")

        if pygame.key.get_pressed()[pygame.K_j]:
            screen_proxy.scroll(-5,0)
        elif pygame.key.get_pressed()[pygame.K_l]:
            screen_proxy.scroll(5, 0)

        screen.fill((135, 206, 235))

        player.move()
        player.draw()
        level.draw()

    elif game_session.get_state() == GameSession.GameSessionState.DEAD:
        print("dead")
        big_font = pygame.font.Font("sprites/font.otf", 96)
        small_font = pygame.font.Font("sprites/font.otf", 32)

        death_message_surface = big_font.render("You Died!", True, (0, 0, 0))
        respawn_message_surface = small_font.render("Press space to respawn", True, (0, 0, 0))
        title_screen_message_surface = small_font.render("Press any other key for title screen", True, (0, 0, 0))

        screen.fill((255, 76, 76))

        screen.blit(death_message_surface, (100,100))
        screen.blit(respawn_message_surface, (120,240))
        screen.blit(title_screen_message_surface, (20,340))

        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                player.reset()
            elif event.type == pygame.KEYDOWN:
                game_session.change_state(GameSession.GameSessionState.TITLE_SCREEN)

    if game_session.get_state() == GameSession.GameSessionState.TITLE_SCREEN:
        print("title")
        big_font = pygame.font.Font("sprites/font.otf", 96)
        small_font = pygame.font.Font("sprites/font.otf", 32)
        mini_font = pygame.font.Font("sprites/font.otf", 24)

        title_screen_message_surface = big_font.render("Potato", True, (0, 0, 0))
        title_screen_play_message = small_font.render("Press space to play", True, (0, 0, 0))
        warning_message_surface = mini_font.render("Sorry, the keys could be unresponsive", True, (0, 0, 0))

        screen.fill((150, 255, 150))

        screen.blit(title_screen_message_surface, (180, 100))
        screen.blit(title_screen_play_message, (170, 220))
        screen.blit(warning_message_surface, (100, 280))

        level.draw()

        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                player.reset()

    player.process_hp()

    pygame.display.flip()
    Clock.tick(60)

pygame.quit()
sys.exit()