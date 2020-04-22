import tcod as libtcod

#스크린 가로/세로 크기
screen_width = 40
screen_height = 25

#지도
map_width = 20
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
    'light_wall': libtcod.Color(130, 110, 50),
    'light_ground': libtcod.Color(200, 180, 50),
    'pitch_black': libtcod.Color(0,0,0,)
}