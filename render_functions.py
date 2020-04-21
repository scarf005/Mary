import tcod as libtcod
from camera import Camera

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors, camera):
    # 좌표를 카메라 기준 좌표로 함
    """
    카메라 따라가기 기능 추가: 주석 싹 다 바꾸어야 함
    """
    # 지도에 있는 모든 타일을 그림
    for y in range(game_map.height):
        for x in range(game_map.width):
            map_x = x + camera.x 
            map_y = y + camera.y
            # visible 불리언에 좌표가 시야에 들어오는지 여부를 대입한다.
            # wall 불리언에 tile의 block_sight이 True인지 False인지를 여부를 대입한다.
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            wall = game_map.tiles[x][y].block_sight

            #타일이 시야 안에 들어올 때
            if visible:
                # 타일이 벽 (True) 이면 짙은 색, 바닥 (False) 이면 옅은 색깔로 출력한다.
                if wall:
                    libtcod.console_set_char_background(con, map_x, map_y, colors.get('light_wall'), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, map_x, map_y, colors.get('light_ground'), libtcod.BKGND_SET)
                # 타일의 상태를 "탐험함(이 타일을 본 적 있음)으로 바꿈"
                game_map.tiles[x][y].explored = True
            #타일이 시야 안에 없지만 탐험한 적이 있을 때 표시 (전장의 안개)
            elif game_map.tiles[x][y].explored:
                if wall:
                    libtcod.console_set_char_background(con, map_x, map_y, colors.get('dark_wall'), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, map_x, map_y, colors.get('dark_ground'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, map_x, map_y, colors.get('outside_camera'), libtcod.BKGND_SET)

    # 목록에 있는 모든 객체를 표시한다.
    for entity in entities:
        draw_entity(con, entity, fov_map, camera)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities, camera):
    # 목록에 있는 모든 객체를 제거한다.
    for entity in entities:
        clear_entity(con, entity, camera)

def draw_entity(con, entity, fov_map, camera):
    #시야 안에 객체가 들어올 때만 객체를 그림
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        # 객체를 표시함. 앞줄은 글자색, 뒷줄은 글자 배치.
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x + camera.x, entity.y + camera.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity, camera):
    # 객체를 화면에서 지운다
    libtcod.console_put_char(con, entity.x + camera.x, entity.y + camera.y, ' ', libtcod.BKGND_NONE)