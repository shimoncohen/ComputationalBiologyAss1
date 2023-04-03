import pygame
from pygame.locals import *

from graphics_utils import InputBox
from shapes import Button

pygame.init()

screen = pygame.display.set_mode((800, 600))

gameOn = True
# Set background color to white
background_color = pygame.color.Color('#FFFFFF')

L_input_box = InputBox(170, 100, 50, 40, label="L:")
p_input_box = InputBox(170, 150, 50, 40, label='P:')
grid_size_input_box = InputBox(170, 200, 50, 40, label='Grid Size:')

input_boxes = [
    L_input_box,
    p_input_box,
    grid_size_input_box
]

start_button = Button(350, 400, 150, 100, label='START')

while gameOn:

    for event in pygame.event.get():
        for input_box in input_boxes:
            input_box.handle_event(event)
            input_box.update()

        start_button.handle_event(event)

        if start_button.active:
            for input_box in input_boxes:
                input_box.set_value()

        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # Check for QUIT event
            pass

        if event.type == QUIT:
            gameOn = False

    screen.fill(background_color)
    for input_box in input_boxes:
        input_box.draw(screen)

    start_button.draw(screen)

    pygame.display.flip()
