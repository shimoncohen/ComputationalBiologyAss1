import pygame

from src.ui.menu_window import MenuWindow
from src.ui.grid_window import GridWindow

pygame.init()

h = 600
w = 600
screen = pygame.display.set_mode((w, h))

curr_window = MenuWindow(h, w, screen)

while curr_window.game_on:
    if curr_window.change_window:
        if isinstance(curr_window, MenuWindow):
            menu_boxes_val = curr_window.get_boxes_vals()

            if curr_window.validate_positive():
                if 0 <= 1 - sum(menu_boxes_val['doubt_probs']) < 1e-5:
                    curr_window = GridWindow(h, w, screen,
                                             curr_window.grid_size_input_box.get_value(),
                                             display_offset=40,
                                             render_cooldown=curr_window.render_time_input_box.get_value(),
                                             **menu_boxes_val)
            else:
                curr_window.reset_buttons_status()
        else:
            curr_window = MenuWindow(h, w, screen)

    curr_window.render()
    pygame.display.flip()

    for event in pygame.event.get():
        curr_window.update(event)

