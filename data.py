import tcod

#폰트
font_width = 16
font_height = 16

TILESET_TTF = tcod.tileset.load_truetype_font('NGCB.ttf', font_width, font_height)

#스크린 가로/세로 크기
screen_width = 42
screen_height = 35

WIDTH = int(screen_width * font_width)
HEIGHT = int(screen_height * font_height)

#지도
map_width = 42
map_height = 25


"""
인터페이스
"""
# 체력 바
bar_width = 20
panel_height = screen_height - map_height
panel_y = screen_height - panel_height

message_x = 1
message_width = screen_width - 2 #- bar_width - 2
message_height = panel_height - 2 #1

#FOV
fov_algorithm_lit = 2
fov_algorithm_dark = 3
fov_light_walls = True
max_fov_radius = 12

#광원
light_radius = 3

#타일 색깔
colors = {
    'dark_wall': tcod.Color(0, 0, 100),
    'dark_ground': tcod.Color(50, 50, 150),
    'light_wall': tcod.Color(50, 50, 30),
    'light_ground': tcod.Color(60, 60, 40),
    'pitch_black': tcod.Color(0,0,0),
    'explosion': tcod.Color(255, 52, 20),
    'flash' : tcod.Color(74, 177, 255),
    '*ambient_light' : -30
}

