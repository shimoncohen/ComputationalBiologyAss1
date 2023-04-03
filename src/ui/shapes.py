import pygame as pg

from .colors import RED_COLOR, WHITE_COLOR

pg.init()

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class Button:
    def __init__(self, x, y, w, h, font_size=32, label=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = RED_COLOR
        self.label = label
        self.font_size = font_size
        self.font = pg.font.Font(None, self.font_size)
        self.label_surface = self.font.render(self.label, True, WHITE_COLOR)
        self.active = False

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, border_radius=5)
        # Blit the text.
        screen.blit(self.label_surface,
                    (self.rect.x+self.rect.w/2 - self.font_size,
                     self.rect.y+self.rect.h/2 - self.font_size/2)
                    )

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False