from .window import Window
from .graphics_utils import InputBox, CheckBox, DropDown
from .shapes import Button
from .colors import WHITE_COLOR, BLACK_COLOR, COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_ACTIVE, COLOR_LIST_INACTIVE

import pygame as pg


class MenuWindow(Window):
    def __init__(self, h, w, screen):
        super().__init__(h, w, screen)
        self.L_input_box = InputBox(170, 30, 50, 40, label="L:", text='5')
        self.p_input_box = InputBox(170, 80, 50, 40, label='P:', text='0.5')
        self.grid_size_input_box = InputBox(170, 130, 50, 40, label='Grid Size:', text='100')
        self.checkbox = CheckBox(220, 180, 40, 40, 32, BLACK_COLOR, label='Wrap Around: ')
        self.neighbors_dropdown = DropDown(
            50, 240, 200, 30,
            pg.font.Font(None, 20),
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            "Neighbors Mode: ",
            ["All", "Cross", "Diagonal"])

        self.input_boxes = [
            self.L_input_box,
            self.p_input_box,
            self.grid_size_input_box
        ]

        self.start_button = Button(200, 400, 150, 100, label='START')
        self.change_window = False

    def update(self, event):
        super().update(event)
        for input_box in self.input_boxes:
            input_box.handle_event(event)
            input_box.update()

        self.neighbors_dropdown.update()

        self.checkbox.handle_event(event)
        self.start_button.handle_event(event)
        self.neighbors_dropdown.handle_event(event)

        if self.start_button.active:
            for input_box in self.input_boxes:
                input_box.set_value()
            self.neighbors_dropdown.set_value()

        if self.start_button.active:
            self.change_window = True

    def render(self):
        self.screen.fill(WHITE_COLOR)
        self.start_button.draw(self.screen)

        for input_box in self.input_boxes:
            input_box.draw(self.screen)

        self.neighbors_dropdown.draw(self.screen)
        self.checkbox.draw(self.screen)

    def get_boxes_vals(self):
        d = {b.get_name(): b.get_value() for b in self.input_boxes}
        d.update(self.checkbox.get_status())
        d.update({self.neighbors_dropdown.get_name(): self.neighbors_dropdown.get_value()})
        return d