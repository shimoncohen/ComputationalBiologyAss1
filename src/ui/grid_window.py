from time import sleep

import pygame as pg

from .window import Window
from .colors import BLACK_COLOR, WHITE_COLOR, RED_COLOR, GREEN_COLOR, YELLOW_COLOR
from src.backend.board import Board
from .in_game_menu import InGameMenu


class GridWindow(Window):
    def __init__(self, h: int,
                 w: int,
                 screen: pg.display,
                 num_blocks: int,
                 display_offset: int,
                 **kwargs
                 ):
        super().__init__(h, w, screen)
        self.n_blocks = int(num_blocks)
        self.display_offset = display_offset
        self.board = Board(kwargs['L'], kwargs['wrap_around'])
        self.board.initialize(self.n_blocks, self.n_blocks, kwargs['P'], kwargs['doubt_probs'])
        self.block_h = int((self.h - self.display_offset) / self.n_blocks)
        self.block_w = int(self.w / self.n_blocks)
        self.change_window = False
        self.in_game_menu = InGameMenu(26, self.display_offset, w, YELLOW_COLOR)
        self.should_run = True

    def draw_grid(self) -> None:
        self.screen.fill(WHITE_COLOR)
        self._color_people()
        self._color_rumors()

    def _color_people(self) -> None:
        rows, cols = self.board.people.shape

        for r in range(rows):
            for c in range(cols):
                person = self.board.people[r, c]

                rect = pg.Rect(c * self.block_w, self.display_offset + r * self.block_h, self.block_w, self.block_h)
                if person:
                    pg.draw.rect(self.screen, RED_COLOR, rect)

                pg.draw.rect(self.screen, BLACK_COLOR, rect, 1)

    def _color_rumors(self) -> None:
        pass

    def render(self, event) -> None:
        super().render(event)
        self.draw_grid()
        self.in_game_menu.draw(self.screen)
        if self.should_run:
            self.board.run_once()
            self.in_game_menu.update()

        # pg.time.wait(1000)