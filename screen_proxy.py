import pygame

class ScreenProxy:
    def __init__(self, screen: pygame.Surface, level_box: pygame.rect):
        self._screen = screen
        self._proxy_box = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self._level_box = level_box

    def scroll(self, offset_x_change: float, offset_y_change: float) -> tuple[int, int]:
        self._proxy_box.move_ip(offset_x_change, offset_y_change)
        if self._proxy_box.union(self._level_box) != self._level_box:
            self._proxy_box.move_ip(-offset_x_change, -offset_y_change)
            return 0, 0
        return self._proxy_box.x, self._proxy_box.y

    def blit(self, image: pygame.Surface, x: float, y: float) -> None:
        blit_box = pygame.Rect(x, y , image.get_width(), image.get_height())
        if blit_box.colliderect(self._proxy_box):
            self._screen.blit(image, (x - self._proxy_box.x, y - self._proxy_box.y))

