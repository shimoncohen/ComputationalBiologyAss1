from typing import List

import pygame as pg
from pygame.locals import *


class Window:
    def __init__(self, h, w, screen):
        self.h = h
        self.w = w
        self.screen = screen

        self.game_on = True

    def update(self, event):
        if event.type == QUIT:
            self.game_on = False

    def change_cursor(self, collisions: List[bool]) -> None:
        if any(collisions):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
