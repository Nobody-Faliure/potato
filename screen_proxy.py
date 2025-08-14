import pygame


class ScreenProxy:
    def __init__(self,
                 screen: pygame.Surface,
                 world_box: pygame.rect,
                 screen_width: int):
        self._screen = screen
        self._proxy_box = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self._world_box = world_box
        self._scroll_buff = 120
        self._scroll_counter = 0
        self._screen_width = screen_width
        self._scroll_counter = 0
        self._scroll_range = 160
        self._scroll_cooldown = 0

    def scroll(self, offset_x_change: float, offset_y_change: float) -> tuple[int, int]:
        self._proxy_box.move_ip(offset_x_change, offset_y_change)
        if self._proxy_box.union(self._world_box) != self._world_box:
            self._proxy_box.move_ip(-offset_x_change, -offset_y_change)
            return 0, 0
        return self._proxy_box.x, self._proxy_box.y

    def revert(self) -> None:
        self._proxy_box.x = 0
        self._proxy_box.y = 0
        self._scroll_cooldown = 0

    def blit(self, surface: pygame.Surface, x: float, y: float) -> None:
        blit_box = pygame.Rect(x, y , surface.get_width(), surface.get_height())
        if blit_box.colliderect(self._proxy_box):
            self._screen.blit(surface, (x - self._proxy_box.x, y - self._proxy_box.y))

    def get_proxy_box(self) -> pygame.Rect:
        return self._proxy_box

    def process_scrolling(self, player_box: pygame.rect, screen_width: int):
        if self._scroll_counter < 0:
            self.scroll(-5, 0)
            self._scroll_counter += 1
            if self._scroll_counter == 0:
                self._scroll_cooldown = 300
        elif self._scroll_counter > 0:
            self.scroll(5, 0)
            self._scroll_counter -= 1
            if self._scroll_counter == 0:
                self._scroll_cooldown = 120
        else:
            if self._scroll_cooldown > 0:
               self._scroll_cooldown -= 1
            if player_box.x < self.get_proxy_box().x + self._scroll_range and self._scroll_cooldown == 0:
                self.scroll(-5, 0)
                self._scroll_counter = -96
            elif player_box.x > self.get_proxy_box().x + screen_width - self._scroll_range and self._scroll_cooldown == 0:
                self.scroll(5, 0)
                self._scroll_counter = 96
