from typing import List

import pygame as pg

from src.ui.window import Window
from src.ui.graphics_utils import InputBox, CheckBox, DropDown, FilePrompt, Button
from src.ui.colors import WHITE_COLOR, BLACK_COLOR, COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_ACTIVE, COLOR_LIST_INACTIVE, RED_COLOR, GREY_COLOR


class MenuWindow(Window):
    def __init__(self, h, w, screen):
        super().__init__(h, w, screen)
        self.L_input_box = InputBox(170, 30, 100, 40, label="L:", text='5')
        self.p_input_box = InputBox(170, 80, 100, 40, label='P:', text='0.5')
        self.grid_size_input_box = InputBox(170, 130, 100, 40, label='Grid Size:', text='100')
        self.s1_perc_input_box = InputBox(400, 30, 100, 40, label='S1:', label_x_offset=50, text='0.25')
        self.s2_perc_input_box = InputBox(400, 80, 100, 40, label='S2:', label_x_offset=50, text='0.25')
        self.s3_perc_input_box = InputBox(400, 130, 100, 40, label='S3:', label_x_offset=50, text='0.25')
        self.s4_perc_input_box = InputBox(400, 180, 100, 40, label='S4:', label_x_offset=50, text='0.25')
        self.render_time_input_box = InputBox(420, 230, 80, 40,
                                              label_font_size=32, label='Time : ',
                                              label_x_offset=70,
                                              text='0.5',
                                              text_font_size=32)
        self.checkbox = CheckBox(220, 180, 40, 40, 32, BLACK_COLOR, label='Wrap Around: ')
        self.neighbors_dropdown = DropDown(
            50, 290, 200, 30,
            pg.font.Font(None, 20),
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            "Neighbors Mode: ",
            ["All", "Cross", "Diagonal"])
        self.fileprompt = FilePrompt(
            160, 240, 180, 30,
            font_size=20,
            color=WHITE_COLOR,
            label="Click to load file: "
        )

        self.input_boxes = [
            self.L_input_box,
            self.p_input_box,
            self.grid_size_input_box,
            self.fileprompt
        ]

        self.perc_input_boxes = [
            self.s1_perc_input_box,
            self.s2_perc_input_box,
            self.s3_perc_input_box,
            self.s4_perc_input_box,
        ]

        self.start_button = Button(200, 400, 150, 100, active_color=RED_COLOR, inactive_color=GREY_COLOR, label='START')
        self.change_window = False

    def update(self, event):
        super().update(event)
        for input_box in self.input_boxes:
            input_box.handle_event(event)

        for input_box in self.perc_input_boxes:
            input_box.handle_event(event)

        self.neighbors_dropdown.update()

        self.checkbox.handle_event(event)
        self.start_button.handle_event(event)
        self.neighbors_dropdown.handle_event(event)
        self.render_time_input_box.handle_event(event)

        if 0 <= 1 - sum([box.value for box in self.perc_input_boxes]) < 1e-5 and self.validate_positive():
            self.start_button.available = True
        else:
            self.start_button.available = False

        if self.start_button.active:
            for input_box in self.input_boxes:
                input_box.set_value()

            for input_box in self.perc_input_boxes:
                input_box.set_value()

            self.neighbors_dropdown.set_value()
            self.render_time_input_box.set_value()

            self.change_window = True

        cols = self.get_collisions(event)
        self.change_cursor(cols)

    def render(self):
        self.screen.fill(WHITE_COLOR)
        self.start_button.draw(self.screen)

        for input_box in self.input_boxes:
            input_box.draw(self.screen)

        for input_box in self.perc_input_boxes:
            input_box.draw(self.screen)

        self.render_time_input_box.draw(self.screen)
        self.neighbors_dropdown.draw(self.screen)
        self.checkbox.draw(self.screen)

    def get_boxes_vals(self):
        d = {b.get_name(): b.get_value() for b in self.input_boxes}
        d.update(self.checkbox.get_status())
        d.update({'doubt_probs': [b.get_value() for b in self.perc_input_boxes]})
        d.update({self.neighbors_dropdown.get_name(): self.neighbors_dropdown.get_value()})
        return d

    def validate_positive(self):
        d = self.get_boxes_vals()
        d.update({'Time': self.render_time_input_box.get_value()})

        for name, val in d.items():
            if name == 'None' or val is None:
                continue

            if type(val) not in [int, float, list]:
                 continue

            if isinstance(val, list):
                for v in val:
                    if v < 0 or v > 1:
                        return False
            else:
                thresh = 0
                if name == 'L':
                    thresh = -1
                if name == 'P':
                    if 0 > val or val > 1:
                        return False
                if val <= thresh:
                    return False

        return True

    def get_collisions(self, event) -> List[bool]:
        cols = []
        for box in self.input_boxes:
            cols.append(box.get_collision(event))
        for box in self.perc_input_boxes:
            cols.append(box.get_collision(event))

        cols.append(self.neighbors_dropdown.get_collision(event))
        cols.append(self.checkbox.get_collision(event))
        cols.append(self.render_time_input_box.get_collision(event))
        cols.append(self.start_button.get_collision(event))

        return cols

    def reset_buttons_status(self):
        self.change_window = False
        self.start_button.active = False