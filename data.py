import tcod as libtcod

#스크린 가로/세로 크기
screen_width = 30
screen_height = 25

#지도
map_width = 25
map_height = 20

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
    'light_wall': libtcod.Color(80, 80, 50),
    'light_ground': libtcod.Color(80, 80, 60),
    'pitch_black': libtcod.Color(0,0,0,)
}