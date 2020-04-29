import tcod
import numpy as np
import sys, warnings

# 게임 지도
from map_objects.game_map import GameMap

# 앤티티와 컴포넌트
from entity import Entity, get_blocking_entities_at_location
from death_functions import kill_monster, kill_player

from components.fighter import Fighter
from components.inventory import Inventory
from components.luminary import Luminary
from components.item import Item
from item_functions import heal, read, talisman


# 렌더링 기능
from renderer.camera import Camera
from renderer.lighting_functions import initialize_light
from renderer.render_functions import clear_all_entities, render_all, RenderOrder
from renderer.fov_functions import initialize_fov, recompute_fov

# 조작 및 기타
from game_messages import Message, MessageLog
from game_states import GameStates
from input_handlers import handle_keys
from debugs import Debug


# 변수 정보
from data import *

if not sys.warnoptions:
    warnings.simplefilter("ignore")

def main():

    """
    객체 생성
    """
    # 플레이어 객체 생성. 위치는 맵 중앙.

    fighter_component = Fighter(hp=30, defense=2, power=5)
    luminary_component = Luminary(luminosity=10)
    inventory_component = Inventory(26)
    player = Entity(int(map_width/2),int(map_height/2),'@',tcod.white, 'You', blocks=True, render_order=RenderOrder.ACTOR, _Luminary=luminary_component, _Fighter=fighter_component, _Inventory=inventory_component)
    entities = [player]

    i_comp = Item(use_function=read,about='about activities of you and your best friend, Mary')
    Journal = Entity(player.x,player.y, ':', tcod.darkest_red,
                     'Swallowstone Journal', render_order=RenderOrder.ITEM, _Item = i_comp)

    i_comp = Item(use_function=talisman)
    Talisman = Entity(player.x,player.y, '*', tcod.lighter_purple,
                      'Passionflower Talisman', render_order=RenderOrder.ITEM, _Item = i_comp)

    player._Inventory.items.append(Journal)
    player._Inventory.items.append(Talisman)

    # 지도 객체 생성: y,x 순서는 game_map 객체에서 알아서 처리
    game_map = GameMap(map_width,map_height)
    game_map.create_map_cave(entities, 3, 10, 6)

    # FOV
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    # 광원, light_map은 numpy 리스트

    light_recompute = True

    light_map = initialize_light(game_map, fov_map, entities)

    # 카메라 객체 생성
    camera = Camera(0,0, map_width, map_height, True)

    camera.update(player)

    """
    디버그 명령 목록
    passwall: 벽 통과 가능
    showpos: 플레이어 x,y좌표 표시. 다른 엔티티 좌표도 표시할 수 있게 고칠 것
    """
    # 디버그용 객체 생성. 디버그 기능들은 기본적으로 꺼져 있고, 인자를 넣으면 활성화
    debug = Debug()

    # 메세지 출력용 객체 생성.
    message_log = MessageLog(message_x, message_width, message_height)

    # 키보드, 마우스 입력 처리용 객체 생성
    key = tcod.Key()
    mouse = tcod.Mouse()

    # 순서 결정용 객체 생성
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    # 콘솔, 패널 생성
    con = tcod.console.Console(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    # 폰트 설정: 10x10파일, 이미지 파일은 그레이스케일, 배열 방식은 TCOD
    # tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    # 폰트 설정: 32x32파일, 이미지 파일은 그레이스케일, 배열 방식은 CP437
    tcod.console_set_custom_font('terminal16x16.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)

    # 스크린 생성: 스크린 가로/세로, 이름, 전체화면 여부
    tcod.console_init_root(screen_width, screen_height, 'Mary', False, vsync=True)


    # TCOD 루프
    while not tcod.console_is_window_closed():
        """
        입력
        """
        # 사용자 입력을 받음: 키 누를 시, 키보드, 마우스
        tcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        """
        화면 표시
        """
        # 플레이어 시야
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)


        if light_recompute:
            light_map = initialize_light(game_map, fov_map, entities)

        """
        화면 표시
        """
        # 화면 초기화
        clear_all_entities(con, entities, camera)

        # 표시할 모든 객체를 화면에 배치함
        render_all(game_state, con, panel, mouse, entities, player,
                   game_map, fov_map, light_map, camera, message_log, fov_recompute,
                   screen_width, screen_height,
                   bar_width, panel_height, panel_y, colors)

        fov_recompute = False
        light_recompute = False

        # 화면 출력
        tcod.console_flush()

        # 화면 초기화
        clear_all_entities(con, entities, camera)

        """
        입력에 대한 상호작용
        """
        # action 변수에 키보드 입력값을 사전 형태로 받아옴
        action = handle_keys(key, game_state)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        drop_inventory = action.get('drop_inventory')

        toggle_light = action.get('toggle_light')
        toggle_wall  = action.get('toggle_wall')
        exit = action.get('exit')

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
                return True

        # 최대화면이 True일 시, 전체화면이 아니라면 콘솔을 전체화면으로 전환함
        if action.get('fullscreen'):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        """
        플레이어 차례에 플레이어가 할 수 있는 행동들
        """
        player_turn_results = []

        # move변수에 대입된 값이 있을 시 이동
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = action.get('move')
            destix = player.x + dx
            destiy = player.y + dy

            if debug.passwall == False:
                if not game_map.is_blocked(destix, destiy):
                    target = get_blocking_entities_at_location(entities, destix, destiy)

                    if target:
                        attack_results = player._Fighter.attack(target)
                        player_turn_results.extend(attack_results)

                    else:
                        player.move(dx, dy)
                        camera.update(player)
                        fov_recompute = True
                        light_recompute = True

                    game_state = GameStates.ENEMY_TURN
            else:
                if game_map.is_blocked(player.x + dx, player.y + dy):
                    debug.dbg_msg("You magically pass through solid wall.")
                player.move(dx, dy)
                camera.update(player)

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity._Item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player._Inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.log(Message('There is nothing here to pick up.', tcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player._Inventory.items):
            item = player._Inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player._Inventory.use(item))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player._Inventory.drop_item(item))

        if toggle_light:
            if player._Luminary.luminosity:
                player._Luminary.luminosity = 0
            else:
                player._Luminary.luminosity = player._Luminary.init_luminosity
            light_recompute = True

        for r in player_turn_results:
            message = r.get('message')
            dead_entity = r.get('dead')
            item_added = r.get('item_added')
            item_consumed = r.get('consumed')
            item_used = r.get('used')
            item_dropped = r.get('item_dropped')

            if message:
                message_log.log(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.log(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed or item_used:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

        """
        적의 차례에 적이 할 수 있는 행동들
        """
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.name == 'light source':
                    pass
                    #message_log.log(F"The {entity.name} is glowing")
                elif entity._Ai:
                    enemy_turn_results = entity._Ai.take_turn(player,
                                                              fov_map, game_map, entities)

                    for er in enemy_turn_results:
                        message = er.get('message')
                        dead_entity = er.get('dead')

                        if message:
                            message_log.log(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.log(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                                break

            else:
                game_state = GameStates.PLAYERS_TURN


        """
        디버그 기능들
        """
        # 플레이어 위치 표시
        if debug.showpos: debug.show_pos(player,'player')

        # 벽 설치
        if toggle_wall:
            game_map.toggle_wall(player.x, player.y)
            # 지형이 변했으니 새로 지형 맵을 짜야 함
            fov_map = initialize_fov(game_map)
            light_recompute = True

        if toggle_light:
            game_map.create_luminary(entities, player.x, player.y, 15)
            # 광원이 새로 생겼으니 다시 계산
            light_recompute = True


if __name__ == '__main__':
    main()