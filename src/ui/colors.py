import pygame as pg

pg.init()
BLACK_COLOR = pg.color.Color('#000000')
WHITE_COLOR = pg.color.Color('#FFFFFF')
RED_COLOR = pg.color.Color('#FF0000')
GREEN_COLOR = pg.color.Color('#00FF00')
BLUE_COLOR = pg.color.Color('#0000FF')
YELLOW_COLOR = pg.color.Color('#FFFF00')

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

def color_from_hex(hex: str) -> pg.color.Color:
    return pg.color.Color(hex)