from .window import Window
from .graphics_utils import InputBox
from .shapes import Button
from .colors import WHITE_COLOR


class MenuWindow(Window):
    def __init__(self, h, w, screen):
        super().__init__(h, w, screen)
        self.L_input_box = InputBox(170, 100, 50, 40, label="L:", text='5')
        self.p_input_box = InputBox(170, 150, 50, 40, label='P:', text='0.5')
        self.grid_size_input_box = InputBox(170, 200, 50, 40, label='Grid Size:', text='100')

        self.input_boxes = [
            self.L_input_box,
            self.p_input_box,
            self.grid_size_input_box
        ]

        self.start_button = Button(200, 400, 150, 100, label='START')
        self.change_window = False

    def render(self, event):
        super().render(event)

        for input_box in self.input_boxes:
            input_box.handle_event(event)
            input_box.update()

        self.start_button.handle_event(event)

        if self.start_button.active:
            for input_box in self.input_boxes:
                input_box.set_value()

        self.screen.fill(WHITE_COLOR)

        for input_box in self.input_boxes:
            input_box.draw(self.screen)

        self.start_button.draw(self.screen)

        if self.start_button.active:
            self.change_window = True

    def get_boxes_vals(self):
        return {b.get_name(): b.get_value() for b in self.input_boxes}