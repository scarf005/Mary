import tcod

from enum import Enum

from yaml_functions import read_yaml

from renderer.lighting_functions import mix_rgb
from data import colors
from game_states import GameStates
from menus import inventory_menu

SYS_LOG = read_yaml("system_log.yaml")

class RenderOrder(Enum):
    # 높을수록 위에 표시한다. 즉 높이
    PORTAL = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    #print(panel)
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    panel.print(int(x + total_width / 2), y, f'{name}: {value}/{maximum}')

def get_names_under_mouse(mouse, camera, entities, fov_map):
    #카메라
    (x, y) = (mouse[0] - camera.x, mouse[1] - camera.y)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and fov_map.fov[entity.y, entity.x]]
    names = ', '.join(names)

    return names.capitalize()

def draw_animation(con, camera, screen_width, screen_height, x, y, color):
    MapX = x + camera.x
    MapY = y + camera.y
    draw_background(con, MapX, MapY, color, 30)

def render_all(game_state, root, con, panel, entities, player, mouse,
               game_map, fov_map, light_map,camera, message_log, fov_recompute,
               screen_width, screen_height, bar_width, panel_height, panel_y, colors):
    if fov_recompute:
        con.clear()
        for y in range(game_map.height):
            for x in range(game_map.width):
                # 지도 위치
                Mapx = x + camera.x
                Mapy = y + camera.y

                #print(F"{camera.x},{camera.y}")

                visible = fov_map.fov[y,x]
                wall = game_map.tiles[y,x].block_sight

                if light_map[y,x] == 999: # 다익스트라 알고리즘 최댓값
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
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map, camera)

    tcod.console_set_default_foreground(con, tcod.white)
    con.print(0, 0, f'현재 층: {game_map.depth}')

    tcod.console_blit(con, 0, 0, screen_width, screen_height, root, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)

    tcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 2
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        #tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        panel.print(message_log.x, y, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player._Fighter.hp, player._Fighter.max_hp,
               tcod.light_red, tcod.darker_red)

    render_bar(panel, screen_width- (bar_width+1), 1, bar_width, 'SANITY', player._Fighter.sanity, player._Fighter.cap_sanity,
               tcod.light_blue, tcod.darker_blue)

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    panel.print(1, 0, get_names_under_mouse(mouse, camera, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, root, 0, panel_y)

    # 인벤토리
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = SYS_LOG["inventory_log"]
        else:
            inventory_title = SYS_LOG["drop_log"]
        inventory_menu(root, con, inventory_title, player._Inventory, screen_width-2, screen_width, screen_height)


def clear_all_entities(con, entities, camera):
    # 목록에 있는 모든 객체를 제거한다.
    for entity in entities:
        clear_entity(con, entity, camera)

def draw_entity(con, entity, fov_map, game_map, camera):
    #시야 안에 객체가 들어올 때만 객체를 그림
    if fov_map.fov[entity.y, entity.x] or (entity._Portal and game_map.tiles[entity.y,entity.x].explored):
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