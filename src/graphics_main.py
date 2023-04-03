import pygame

from ui.menu_window import MenuWindow
from ui.grid_window import GridWindow

pygame.init()

h = 800
w = 600
screen = pygame.display.set_mode((h, w))

curr_window = MenuWindow(h, w, screen)

while curr_window.game_on:
    if curr_window.change_window:
        curr_window = GridWindow(h, w, screen, curr_window.grid_size_input_box, 50, None)

    for event in pygame.event.get():
        curr_window.render(event)

    pygame.display.flip()
