from typing import List

import pygame as pg
from src.ui.window import Window
from src.ui.colors import BLACK_COLOR, WHITE_COLOR, RED_COLOR, GREEN_COLOR, YELLOW_COLOR
from src.backend.board import Board
from src.ui.in_game_menu import InGameMenu
from src.backend.person import DoubtLevel
from src.ui.graphics_utils import FilePrompt


class GridWindow(Window):
    def __init__(self, h: int,
                 w: int,
                 screen: pg.display,
                 num_blocks: int,
                 display_offset: int,
                 render_cooldown: float,
                 **kwargs
                 ):
        super().__init__(h, w, screen)
        self.n_blocks_w = int(num_blocks)
        self.n_blocks_h = int(num_blocks)
        self.display_offset = display_offset
        self.board = Board(kwargs['wrap_around'], kwargs['neighbour_count_type'])
        if 'config_file_path' in kwargs:
            self.board.load(kwargs['config_file_path'])
            n_rows, n_cols = self.board.shape
            self.n_blocks_w = n_cols
            self.n_blocks_h = n_rows
        else:
            self.board.initialize(self.n_blocks_h, self.n_blocks_w, kwargs['L'], kwargs['P'], kwargs['doubt_probs'])
        self.block_h = int((self.h - self.display_offset) / self.n_blocks_h)
        self.block_w = int(self.w / self.n_blocks_w)
        self.change_window = False
        self.in_game_menu = InGameMenu(26, self.display_offset, w, YELLOW_COLOR)
        self.person_font = pg.font.Font(None, 14)
        self.should_run = True
        self.render_cooldown = int(render_cooldown * 1000)
        self.curr_tick = pg.time.get_ticks()

    def draw_grid(self) -> None:
        self.screen.fill(WHITE_COLOR)
        self._color_people()
        self._color_rumors()
        if self.n_blocks_h <= 40 or self.n_blocks_w <= 40:
            self._render_doubt_level()

    def _render_doubt_level(self) -> None:
        rows, cols = self.board.people.shape

        for r in range(rows):
            for c in range(cols):
                person = self.board.people[r, c]
                if person:
                    rect = pg.Rect(c * self.block_w, self.display_offset + r * self.block_h, self.block_w, self.block_h)
                    text = self.person_font.render(DoubtLevel.map_to_str(person.doubt_level), True, BLACK_COLOR)
                    text_rect = text.get_rect()
                    text_rect.center = (rect.x + rect.w / 2, rect.y + rect.h / 2)
                    self.screen.blit(text, text_rect)

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
        self.in_game_menu.handle_event(event)

        if self.in_game_menu.stop_game:
            self.change_window = True

        if self.in_game_menu.save_history_button.active:
            try:
                self.board.save_history(FilePrompt.prompt_save_file())
            except Exception:
                pass
            self.in_game_menu.save_history_button.deactivate()

        cols = self.get_collisions(event)
        self.change_cursor(cols)

    def render(self) -> None:
        now_tick = pg.time.get_ticks()

        if now_tick - self.curr_tick >= self.render_cooldown:
            if self.should_run:
                self.should_run = self.board.run_once()
                self.in_game_menu.update()

            self.draw_grid()
            self.in_game_menu.draw(self.screen)
            self.curr_tick = now_tick

    def get_collisions(self, event) -> List[bool]:
        cols = []
        cols.append(self.in_game_menu.back_to_menu_button.get_collision(event))
        cols.append(self.in_game_menu.save_history_button.get_collision(event))

        return cols