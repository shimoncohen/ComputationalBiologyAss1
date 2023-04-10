import pygame as pg

from .shapes import Button
from .colors import BLACK_COLOR


class InGameMenu:
    def __init__(self,
                 font_size: int,
                 display_offset: int,
                 w: int,
                 color: pg.color.Color
                 ):
        self.font_size = font_size
        self.h = display_offset
        self.w = w
        self.font = pg.font.Font(None, self.font_size)
        self.generations = 0
        self.generations_txt_surface = self.font.render(f'Gen: {self.generations}', True, BLACK_COLOR)
        self.menu_rect_surface = pg.Rect(0, 0, w, display_offset)
        self.color = color
        self.back_to_menu_button = Button(
            self.w / 2, self.h / 4, self.w / 4, 2 * self.h / 3,
            font_size=30, label="Main Menu", label_x_offset=-20
        )
        self.stop_game = False

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.menu_rect_surface)

        screen.blit(self.generations_txt_surface, (self.h / 2 - 5, self.h / 2 - 5))
        self.back_to_menu_button.draw(screen)

    def handle_event(self, event):
        self.back_to_menu_button.handle_event(event)

    def update(self):
        self.generations += 1
        self.generations_txt_surface = self.font.render(f'Gen: {self.generations}', True, BLACK_COLOR)

        if self.back_to_menu_button.active:
            self.stop_game = True
