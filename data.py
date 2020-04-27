import tcod as libtcod

#스크린 가로/세로 크기
screen_width = 50
screen_height = 40

#지도
map_width = 25
map_height = 20

#인터페이스
bar_width = 20
panel_height = 7
panel_y = screen_height - panel_height

message_x = bar_width + 2
message_width = screen_width - bar_width - 2
message_height = panel_height - 1

#FOV
fov_algorithm = 2
fov_light_walls = True
fov_radius = 12

#광원
light_radius = 3

#타일 색깔
colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
    'light_wall': libtcod.Color(50, 50, 30),
    'light_ground': libtcod.Color(60, 60, 40),
    'pitch_black': libtcod.Color(0,0,0,)
}

