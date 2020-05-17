import tcod

from enum import Enum

from yaml_functions import read_yaml

from renderer.lighting_functions import mix_rgb
from init_constants import colors
from enums.game_states import GameStates
from menus import inventory_menu, character_screen

from init_constants import *

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
    panel.print(x, y, f'{name}: {value}/{maximum}') #total_width / 2

def get_names_under_mouse(mouse, camera, entities, fov_map):
    #카메라
    (x, y) = (mouse.x - camera.x - CENTER_X, mouse.y - camera.y - CENTER_Y)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and fov_map.fov[entity.y, entity.x]]
    names = ', '.join(names)

    if not names:
        names = str((x,y))

    return names.capitalize()

def render_all(game_state, root, con, panel, entities, player, mouse,
               game_map, fov_map, light_map, camera, message_log, fov_recompute):
    if fov_recompute:
        con.clear()
        for y in range(game_map.height):
            for x in range(game_map.width):
                # 지도 위치
                Mapx = x + camera.x + CENTER_X
                Mapy = y + camera.y + CENTER_Y

                visible = fov_map.fov[y,x]
                wall = game_map.tiles[y,x].block_sight

                if light_map[y,x] == 999: # 다익스트라 알고리즘 최댓값
                    brightness = 0
                else:
                    brightness = light_map[y,x]

                if visible: # 눈에 보일 때
                    game_map.tiles[y,x].explored = True
                    if wall:
                        draw_background(con, Mapx, Mapy, 'light_wall', brightness)
                    else:
                        draw_background(con, Mapx, Mapy, 'light_ground', brightness)
                elif game_map.tiles[y,x].explored: # 한번 들렀을 때
                    if wall:
                        draw_background(con, Mapx, Mapy, 'dark_wall')
                    else:
                        draw_background(con, Mapx, Mapy, 'dark_ground')
                else:   # 시야 밖일 때
                    draw_background(con, Mapx, Mapy, 'pitch_black')


    # 목록에 있는 모든 객체를 표시함.
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map, camera)

    con.print(0, 0, f"{SYS_LOG['depth']} {game_map.depth}", fg=tcod.white)

    tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, root, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)

    tcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 2
    for message in message_log.messages:
        panel.print(message_log.x, y, message.text, fg=message.color)
        y += 1

    render_bar(panel, 1, 1, BAR_WIDTH, SYS_LOG['hp'], player._Fighter.hp, player._Fighter.max_hp,
               tcod.light_red, tcod.darker_red)

    render_bar(panel, SCREEN_WIDTH- (BAR_WIDTH + 1), 1, BAR_WIDTH, SYS_LOG['sanity'], player._Fighter.sanity, player._Fighter.cap_sanity,
               tcod.light_blue, tcod.darker_blue)

    panel.print(1, 0, get_names_under_mouse(mouse, camera, entities, fov_map), fg=tcod.light_gray)

    tcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, root, 0, PANEL_Y)

    # 인벤토리
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = SYS_LOG["inventory_log"]
        else:
            inventory_title = SYS_LOG["drop_log"]
        inventory_menu(root, con, inventory_title, player._Inventory)

    # 플레이어 정보
    if game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root, con, SYS_LOG['character_info_log']['header'],
                         player=player, game_map=game_map)


def clear_all_entities(con, entities, camera):
    # 목록에 있는 모든 객체를 제거한다.
    for entity in entities:
        clear_entity(con, entity, camera)

def draw_entity(con, entity, fov_map, game_map, camera):
    #시야 안에 객체가 들어올 때만 객체를 그림
    if fov_map.fov[entity.y, entity.x] or (entity._Portal and game_map.tiles[entity.y,entity.x].explored):
        # 객체를 표시함. 앞줄은 글자색, 뒷줄은 글자 배치.
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x + camera.x + CENTER_X, entity.y + camera.y + CENTER_Y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity, camera):
    # 객체를 화면에서 지운다
    tcod.console_put_char(con, entity.x + camera.x + CENTER_X, entity.y + camera.y + CENTER_Y, ' ', tcod.BKGND_NONE)

def draw_background(con,x,y,color,brightness=0,flag=None):
    # 나중에 tcod.BKGND_SET이 대체 뭐하는 건지 찾아볼 것
    rgbs = colors.get(color)
    basic_color = tcod.Color(rgbs[0],rgbs[1],rgbs[2])
    total_color = mix_rgb(basic_color,brightness)
    tcod.console_set_char_background(con, x, y, total_color, tcod.BKGND_SET)