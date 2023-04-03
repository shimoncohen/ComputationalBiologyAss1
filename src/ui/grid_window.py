import pygame as pg

from .window import Window
from .colors import BLACK_COLOR, WHITE_COLOR, RED_COLOR, GREEN_COLOR
from backend.board import Board


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
        # self.board.run_once()
        self.drawGrid()