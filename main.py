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
stopped = False

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

big_font = pygame.font.Font("sprites/font.otf", 96)
small_font = pygame.font.Font("sprites/font.otf", 32)
mini_font = pygame.font.Font("sprites/font.otf", 24)

def death_screen():
    you_died_surface = big_font.render("You Died!", True, (0, 0, 0))
    respawn_message_surface = small_font.render("Press space to respawn", True, (0, 0, 0))
    for_title_screen_surface = small_font.render("Press escape key for title screen", True, (0, 0, 0))
    death_message_surface = mini_font.render(player.get_death_message(), True, (0, 0, 100))

    screen.fill((255, 76, 76))

    screen.blit(you_died_surface, (100, 100))
    screen.blit(respawn_message_surface, (120, 280))
    screen.blit(for_title_screen_surface, (40, 380))
    death_message_rect = death_message_surface.get_rect(center=(640 // 2, 220))
    screen.blit(death_message_surface, death_message_rect)

    if key_held[pygame.K_SPACE]:
        player.reset()
    elif key_held[pygame.K_ESCAPE]:
        game_session.change_state(GameSession.GameSessionState.TITLE_SCREEN)

def title_screen():
    title_screen_message_surface = big_font.render("Potato", True, (0, 0, 0))
    title_screen_play_message = small_font.render("Press space to play", True, (0, 0, 0))

    screen.fill((150, 255, 150))

    screen.blit(title_screen_message_surface, (180, 100))
    screen.blit(title_screen_play_message, (170, 220))

    level.draw()

    if key_held[pygame.K_SPACE]:
        game_session.change_state(GameSession.GameSessionState.IN_GAME)
        player.reset()

# Clock
Clock = pygame.time.Clock()

# Main Event Loop
while not stopped:
    # If exit key is pressed set running to false
    key_pressed = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopped = True

    key_held = pygame.key.get_pressed()

    if game_session.get_state() == GameSession.GameSessionState.IN_GAME:
        if key_held[pygame.K_j]:
            screen_proxy.scroll(-5,0)
        elif key_held[pygame.K_l]:
            screen_proxy.scroll(5, 0)

        if key_held[pygame.K_LEFT] or key_held[pygame.K_a]:
            player.move_left()
        elif key_held[pygame.K_RIGHT] or key_held[pygame.K_d]:
            player.move_right()
        if key_held[pygame.K_SPACE]:
            player.jump()

        screen.fill((135, 206, 235))
        player.draw()
        level.draw()

        player.process_hp()

    elif game_session.get_state() == GameSession.GameSessionState.DEAD:
        death_screen()

    elif game_session.get_state() == GameSession.GameSessionState.TITLE_SCREEN:
        title_screen()

    pygame.display.flip()
    Clock.tick(60)

pygame.quit()
sys.exit()