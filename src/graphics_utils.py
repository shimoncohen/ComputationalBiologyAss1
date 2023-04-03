import string

import pygame as pg

from colors import BLACK_COLOR

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class InputBox:
    def __init__(self, x, y, w, h, font_size=32, label=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.label = label
        self.font_size = font_size
        self.font = pg.font.Font(None, self.font_size)
        self.txt_surface = self.font.render(self.text, True, BLACK_COLOR)
        self.label_surface = self.font.render(self.label, True, BLACK_COLOR)
        self.active = False
        self.value = 0

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.unicode in string.printable:
                    self.text += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, BLACK_COLOR)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.label_surface, (self.rect.x-120, self.rect.y+10))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2, border_radius=7)

    def set_value(self):
        self.value = float(self.text)
