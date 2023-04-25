import string
import time
import tkinter
from tkinter import filedialog
from typing import List
import pygame as pg
from src.ui.colors import BLACK_COLOR, COLOR_INACTIVE, COLOR_ACTIVE, RED_COLOR, WHITE_COLOR
from src.ui.shapes import Collidable


class InputBox(Collidable):
    def __init__(self, x, y, w, h,
                 label_font_size=32, label='',
                 label_x_offset=120, label_y_offset=10,
                 text_font_size=32, text=''):
        super(InputBox, self).__init__(pg.Rect(x, y, w, h))
        self.color = COLOR_INACTIVE
        self.text = text
        self.label = label
        self.label_font = pg.font.Font(None, label_font_size)
        self.txt_font = pg.font.Font(None, text_font_size)
        self.txt_surface = self.txt_font.render(self.text, True, BLACK_COLOR)
        self.label_surface = self.label_font.render(self.label, True, BLACK_COLOR)
        self.label_x_offset = label_x_offset
        self.label_y_offset = label_y_offset
        self.active = False
        self.value = 0
        self.cursor = pg.Rect(self.txt_surface.get_rect().topright, (3, self.txt_surface.get_rect().height + 2))

    def handle_event(self, event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.unicode in string.printable:
                    self.text += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Re-render the text.
                self.txt_surface = self.txt_font.render(self.text, True, BLACK_COLOR)

    def update(self) -> None:
        # Resize the box if the text is too long.
        # width = max(self.rect.w, self.txt_surface.get_width()+10)
        # self.rect.w = width
        pass

    def draw(self, screen) -> None:
        # Blit the text.
        screen.blit(self.label_surface, (self.rect.x-self.label_x_offset, self.rect.y+self.label_y_offset))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2, border_radius=7)

        if self.active:
            if time.time() % 1 > 0.5:

                # bounding rectangle of the text
                text_rect = self.txt_surface.get_rect(topleft=(self.rect.x + 5, self.rect.y + 5))

                # set cursor position
                self.cursor.midleft = text_rect.midright

                pg.draw.rect(screen, self.color, self.cursor)

    def set_value(self) -> None:
        try:
            self.value = float(self.text)
        except ValueError:
            return

    def get_value(self):
        return self.value

    def get_name(self):
        return self.label.replace(':', '')


class CheckBox(Collidable):
    def __init__(self,
                 x: int,
                 y: int,
                 h: int,
                 w: int,
                 font_size: int,
                 color: pg.color.Color,
                 label: str = ''
                 ):
        super(CheckBox, self).__init__(pg.Rect(x, y, w, h))
        self.checked = False
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.label = label
        self.inner_rect = pg.Rect(x + 5, y + 5, w - 10, h - 10)
        self.color = color
        self.label = label
        self.font_size = font_size
        self.font = pg.font.Font(None, self.font_size)
        self.label_surface = self.font.render(self.label, True, BLACK_COLOR)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.label_surface, (self.rect.x - 170, self.rect.y + 10))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2, border_radius=7)

        if self.checked:
            pg.draw.rect(screen, COLOR_ACTIVE, self.inner_rect, border_radius=7)

    def handle_event(self, event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.checked = not self.checked

    def get_status(self):
        return {self.label.replace(':', '').strip().replace(' ', '_').lower(): self.checked}


class DropDown(Collidable):
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 font: pg.font.Font,
                 color_menu: List[pg.color.Color],
                 color_option: List[pg.color.Color],
                 main_txt: str,
                 options_txt: List[str]):
        super(DropDown, self).__init__(pg.Rect(x, y, w, h))
        self.color_menu = color_menu
        self.color_option = color_option
        self.font = font
        self.initial_txt = main_txt + options_txt[0]
        self.main = main_txt + options_txt[0]
        self.options = options_txt
        self.draw_menu = False
        self.menu_active = False
        self.active_option = 0
        self.value = self.options[0]

    def draw(self, screen):
        pg.draw.rect(screen, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, True, (0, 0, 0))
        screen.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pg.draw.rect(screen, self.color_option[1 if i + 1 == self.active_option else 0], rect, 0)
                msg = self.font.render(text, True, (0, 0, 0))
                screen.blit(msg, msg.get_rect(center=rect.center))

    def update(self):
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = 0
        for i in range(len(self.options) + 1):
            rect = self.rect.copy()
            rect.y += i * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == 0:
            self.draw_menu = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option > 0:
                self.draw_menu = False
                self.main = f"{self.main.split(':')[0]}:" \
                            f" {self.options[self.active_option - 1] if self.active_option != 0 else self.initial_txt}"
                self.value = self.active_option - 1

    def set_value(self):
        return

    def get_value(self):
        return self.value

    def get_name(self):
        return 'neighbour_count_type'


class FilePrompt(Collidable):
    def __init__(self,
                 x: int,
                 y: int,
                 h: int,
                 w: int,
                 font_size: int,
                 color: pg.color.Color,
                 label: str
                 ):
        super(FilePrompt, self).__init__(pg.Rect(x, y, h, w))
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.font_size = font_size
        self.font = pg.font.Font(None, font_size)
        self.color = color
        self.label = label
        self.txt = '<Click to load config file>'
        self.txt_surface = self.font.render(self.txt, True, BLACK_COLOR)
        self.label_surface = self.font.render(self.label, True, BLACK_COLOR)
        self.value = ''

    @staticmethod
    def prompt_open_file() -> str:
        """Create a Tk file dialog and cleanup when finished"""
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = filedialog.askopenfilename(parent=top)
        top.destroy()
        return file_name


    @staticmethod
    def prompt_save_file() -> str:
        """Create a Tk file dialog and cleanup when finished"""
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = filedialog.asksaveasfile(
            defaultextension='.xlsx',
            filetypes=[
                ('Excel file', '.xlsx'),
                ('CSV file', '.csv'),
                ('All files', '.*')
            ],
            parent=top
        )
        top.destroy()
        return file_name.name

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, BLACK_COLOR, self.rect, 1)
        # Blit the text.
        screen.blit(self.label_surface, (self.rect.x - 110, self.rect.y + 10))
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()

            if self.rect.collidepoint(mpos):
                self.value = FilePrompt.prompt_open_file()
                self.txt = self.value.split('/')[-1]
                self.txt_surface = self.font.render(self.txt, True, BLACK_COLOR)

    def set_value(self):
        pass

    def get_name(self):
        return 'config_file_path' if self.value != '' else 'None'

    def get_value(self):
        return self.value if self.value != '' else None


class Button(Collidable):
    def __init__(self, x, y, w, h, font_size=32, label='', label_x_offset=0, label_y_offset=0):
        super(Button, self).__init__(pg.Rect(x, y, w, h))
        self.color = RED_COLOR
        self.label = label
        self.label_x_offset = label_x_offset
        self.label_y_offset = label_y_offset
        self.font_size = font_size
        self.font = pg.font.Font(None, self.font_size)
        self.label_surface = self.font.render(self.label, True, WHITE_COLOR)
        self.active = False

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, border_radius=5)
        # Blit the text.
        screen.blit(self.label_surface,
                    (self.rect.x+self.rect.w/2 - self.font_size + self.label_x_offset,
                     self.rect.y+self.rect.h/2 - self.font_size/2 + self.label_y_offset)
                    )

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False


class ImageButton(Collidable):
    def __init__(self, x, y, w, h, color, image_path):
        super(ImageButton, self).__init__(pg.rect.Rect(x, y, w, h))
        self.color = color
        self.image = pg.image.load(image_path).convert_alpha()
        self.active = False

    def draw(self, screen):
        img_rect = self.image.get_rect()
        img_rect.center = (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2)

        pg.draw.rect(screen, self.color, self.rect, border_radius=3)
        screen.blit(self.image, img_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

    def deactivate(self):
        self.active = False
