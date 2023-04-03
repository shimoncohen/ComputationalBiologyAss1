import pygame as pg

from .window import Window
from .colors import BLACK_COLOR, WHITE_COLOR, RED_COLOR, GREEN_COLOR
from src.board import Board


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
        self.board = Board(self.n_blocks, self.n_blocks, **kwargs)

        self.block_h = int((self.h - self.display_offset) / self.n_blocks)
        self.block_w = int(self.w / self.n_blocks)

        self.change_window = False

    def drawGrid(self) -> None:
        self.screen.fill(WHITE_COLOR)

        for x in range(0, self.w, self.block_w):
            for y in range(self.display_offset, self.h, self.block_h):
                rect = pg.Rect(x, y, self.block_w, self.block_h)
                pg.draw.rect(self.screen, BLACK_COLOR, rect, 1)

        r=pg.Rect(790, 590, 10, 10)
        pg.draw.rect(self.screen, BLACK_COLOR, r)

        self._color_people()
        self._color_rumors()

    def _color_people(self) -> None:

        for i, x in enumerate(range(0, self.w, self.block_w)):
            for j, y in enumerate(range(self.display_offset, self.h, self.block_h)):
                person = self.board.people[i, j]
                if person:
                    rect = pg.Rect(x, y, self.block_w, self.block_h)
                    pg.draw.rect(self.screen, GREEN_COLOR, rect)
                    pg.draw.rect(self.screen, BLACK_COLOR, rect, 1)

    def _color_rumors(self) -> None:
        pass

    def render(self, event) -> None:
        super().render(event)
        # self.board.run_once()
        self.drawGrid()