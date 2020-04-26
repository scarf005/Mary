import tcod 

from renderer.lighting_functions import mix_rgb
from data import colors

def render_all(con, entities, game_map, fov_map, light_map, camera, fov_recompute, screen_width, screen_height, colors):
    # fov 재계산 시만
    if fov_recompute:
        #tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        con.clear()
        
        for y in range(game_map.height):
            for x in range(game_map.width):
                # 지도 위치
                Mapx = x + camera.x
                Mapy = y + camera.y
                
                #print(F"{camera.x},{camera.y}")
                
                # wall 불리언에 tile의 block_sight이 True인지 여부를 대입                
                visible = fov_map.fov[y,x]
                wall = game_map.tiles[y,x].block_sight
                
                if light_map[y,x] == 999:
                    brightness = 0
                else:
                    brightness = light_map[y,x]
                 
                if visible:
                    game_map.tiles[y,x].explored = True
                    if wall:
                        draw_background(con, Mapx, Mapy, 'light_wall', brightness)
                    else:
                        draw_background(con, Mapx, Mapy, 'light_ground', brightness)                 
                elif game_map.tiles[y,x].explored:
                    if wall:
                        draw_background(con, Mapx, Mapy, 'dark_wall')
                    else:
                        draw_background(con, Mapx, Mapy, 'dark_ground')
                else:
                    draw_background(con, Mapx, Mapy, 'pitch_black')


    # 목록에 있는 모든 객체를 표시함.
    for entity in entities:
        draw_entity(con, entity, fov_map, camera)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all_entities(con, entities, camera):
    # 목록에 있는 모든 객체를 제거한다.
    for entity in entities:
        clear_entity(con, entity, camera)

def draw_entity(con, entity, fov_map, camera):
    #시야 안에 객체가 들어올 때만 객체를 그림
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        # 객체를 표시함. 앞줄은 글자색, 뒷줄은 글자 배치.
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x + camera.x, entity.y + camera.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity, camera):
    # 객체를 화면에서 지운다
    tcod.console_put_char(con, entity.x + camera.x, entity.y + camera.y, ' ', tcod.BKGND_NONE)

def draw_background(con,x,y,color,brightness=0,flag=None):
    # 나중에 tcod.BKGND_SET이 대체 뭐하는 건지 찾아볼 것
    total_color = mix_rgb(colors.get(color),brightness)
    tcod.console_set_char_background(con, x, y, total_color, tcod.BKGND_SET)