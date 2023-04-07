import pygame as pg
from time import sleep
from .window import Window
from .colors import BLACK_COLOR, WHITE_COLOR, RED_COLOR, GREEN_COLOR, YELLOW_COLOR
from src.backend.board import Board
from src.backend.game_logic import NeighbourCountType
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
        self.board = Board(kwargs['L'], kwargs['wrap_around'], NeighbourCountType.ALL)
        self.board.initialize(self.n_blocks, self.n_blocks, kwargs['P'], kwargs['doubt_probs'])
        self.block_h = int((self.h - self.display_offset) / self.n_blocks)
        self.block_w = int(self.w / self.n_blocks)
        self.change_window = False
        self.in_game_menu = InGameMenu(26, self.display_offset, w, YELLOW_COLOR)
        self.should_run = True
        self.render_cooldown = 200
        self.curr_tick = pg.time.get_ticks()

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
        rows, cols = self.board.rumor_board.shape

        for r in range(rows):
            for c in range(cols):
                rumor = self.board.rumor_board[r, c]

                rect = pg.Rect(c * self.block_w, self.display_offset + r * self.block_h, self.block_w, self.block_h)

                if rumor:
                    pg.draw.rect(self.screen, GREEN_COLOR, rect)

                pg.draw.rect(self.screen, BLACK_COLOR, rect, 1)

    def update(self, event):
        super().update(event)

    def render(self) -> None:
        now_tick = pg.time.get_ticks()

        if now_tick - self.curr_tick >= self.render_cooldown:
            if self.should_run:
                self.board.run_once()
                self.in_game_menu.update()

            self.draw_grid()
            self.in_game_menu.draw(self.screen)
            self.curr_tick = now_tick

        # pg.time.wait(1000)