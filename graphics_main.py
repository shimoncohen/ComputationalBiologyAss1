from time import sleep
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
        menu_boxes_val = curr_window.get_boxes_vals()
        curr_window = GridWindow(h, w, screen,
                                 curr_window.grid_size_input_box.value,
                                 display_offset=40, doubt_probs=[0, 1 / 3, 2 / 3, 1],
                                 wrap_around=False, **menu_boxes_val)

    for event in pygame.event.get():
        curr_window.render(event)

    pygame.display.flip()
    sleep(1)
