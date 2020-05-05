import tcod
from yaml_functions import read_yaml

CONFIG = read_yaml("config.yaml","!default")

FLAGS = tcod.context.SDL_WINDOW_RESIZABLE

SCREEN_WIDTH = CONFIG['SCREEN_WIDTH']
SCREEN_HEIGHT = CONFIG['SCREEN_HEIGHT']

WIDTH = int(SCREEN_WIDTH * CONFIG['FONT_WIDTH'])
HEIGHT = int(SCREEN_HEIGHT * CONFIG['FONT_HEIGHT'])
TILESET_TTF = tcod.tileset.load_truetype_font(CONFIG['FONT'],
                                                CONFIG['FONT_WIDTH'],
                                                CONFIG['FONT_HEIGHT'])

MAP_WIDTH, MAP_HEIGHT = CONFIG['MAP_WIDTH'], CONFIG['MAP_HEIGHT']
BAR_WIDTH = CONFIG['BAR_WIDTH']

PANEL_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MESSAGE_X = 1
MESSAGE_WIDTH = SCREEN_WIDTH - 2 #- BAR_WIDTH - 2
MESSAGE_HEIGHT = PANEL_HEIGHT - 2 #1

CENTER_X = int(SCREEN_WIDTH / 2 - MAP_WIDTH / 2)
CENTER_Y = 0 #int(SCREEN_HEIGHT / 2 - MAP_HEIGHT  / 2)

#FOV
fov_algorithm_lit = 2
fov_algorithm_dark = 3
fov_light_walls = True
max_fov_radius = 12

#광원
light_radius = 3

#타일 색깔
colors = CONFIG['COLORS']

