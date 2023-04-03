from pygame.locals import *


class Window:
    def __init__(self, h, w, screen):
        self.h = h
        self.w = w
        self.screen = screen

        self.game_on = True

    def render(self, event):
        if event.type == QUIT:
            self.game_on = False
