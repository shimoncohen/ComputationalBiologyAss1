import pygame as pg

pg.init()


class Collidable:
    def __init__(self, rect: pg.rect.Rect):
        self.rect = rect

    def get_collision(self, event):
        if hasattr(event, 'pos'):
            return self.rect.collidepoint(event.pos)
        else:
            return False