import tcod

#스크린 가로/세로 크기
screen_width = 40
screen_height = 30

#지도
map_width = 40
map_height = 20

"""
인터페이스
"""
# 체력 바
bar_width = 20
panel_height = 7
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

