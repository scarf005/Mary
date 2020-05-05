import tcod
import tcod.event

import numpy as np
import math, random, time

from yaml_functions import read_yaml
from batchim import Batchim


# 게임 지도
from map_objects.game_map import GameMap

# 앤티티와 컴포넌트
from entity import Entity, get_blocking_entities_at_location
from death_functions import kill_monster, kill_player
from item_functions import heal, read, talisman

from components.fighter import Fighter
from components.inventory import Inventory
from components.luminary import Luminary
from components.item import Item

# 렌더링 기능
from renderer.camera import Camera
from renderer.lighting_functions import initialize_light
from renderer.render_functions import clear_all_entities, render_all, RenderOrder
from renderer.fov_functions import initialize_fov, recompute_fov

# 조작 및 기타
from game_messages import Message, MessageLog
from game_states import GameStates
from input_functions import Mouse, Keyboard, handle_input_per_state
from debugs import Debug

# 변수 정보
from data import *

def init_player_and_entities(player_name):
    """
    플레이어
    """

    fighter_component = Fighter(hp=30, sanity=100, defense=2, power=5)
    luminary_component = Luminary(luminosity=10)
    inventory_component = Inventory(26)

    player = Entity(int(map_width/2) , int(map_height/2), '@', tcod.white, player_name , blocks=True, render_order=RenderOrder.ACTOR, _Luminary=luminary_component, _Fighter=fighter_component, _Inventory=inventory_component)
    entities = [player]

    i_comp = Item(use_function=read,
                  about='당신과 당신의 절친, 메리가 같이 한 일들이 적혀 있다') #about activities of you and your best friend, Mary
    Journal = Entity(player.x,player.y, ':', tcod.darkest_red,
                    '수첩', render_order=RenderOrder.ITEM, _Item = i_comp)

    i_comp = Item(use_function=talisman)
    Talisman = Entity(player.x,player.y, '*', tcod.lighter_purple,
                    '시계꽃 부적', render_order=RenderOrder.ITEM, _Item = i_comp)

    player._Inventory.items.append(Journal)
    player._Inventory.items.append(Talisman)

    return player, entities

def init_game_map(player, entities):
    """
    게임 지도
    """
    game_map = GameMap(map_width, map_height)
    game_map.create_map_cave(player, entities, 3)
    game_map.create_portal(entities, 10, player)

    fov_recompute = True
    fov_radius = max_fov_radius
    fov_algorithm = fov_algorithm_lit
    fov_map = initialize_fov(game_map)

    light_recompute = True
    light_map = initialize_light(game_map, fov_map, entities)

    camera = Camera(0,0, map_width, map_height, True)
    camera.update(player)

    return game_map, fov_map, fov_radius, fov_algorithm, fov_recompute, light_recompute, camera

def init_message_and_states():
    """
    메세지 출력
    """
    message_log = MessageLog(message_x, message_width, message_height)

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    targeting_item = None

    return message_log, game_state, previous_game_state, targeting_item

def init_others(*args):
    return Debug(args), Mouse(), Keyboard()

def init_console():
    """
    화면 출력
    """
    context = tcod.context.new_window(WIDTH, HEIGHT,
                            renderer=tcod.context.RENDERER_OPENGL2, tileset=TILESET_TTF,
                            vsync=True, title="MARY")
    console = tcod.Console(map_width, map_height)
    animation = tcod.Console(map_width, map_height)
    panel = tcod.Console(screen_width, panel_height)
    root = tcod.Console(screen_width, screen_height)

    return root, console, panel, context

def init_log():
    SYS_LOG = read_yaml("system_log.yaml")
    return SYS_LOG

def main():
    """
    사전 준비 작업
    """
    SYS_LOG = init_log()

    player, entities = init_player_and_entities(SYS_LOG['player_name'])

    game_map, fov_map, fov_radius, \
    fov_algorithm, fov_recompute, light_recompute, camera = init_game_map(player, entities)

    message_log, game_state, previous_game_state, targeting_item = init_message_and_states()

    root, console, panel, context = init_console()

    debug, mouse, keyboard = init_others()

    quit = False

    """
    메인 루프
    """
    while not quit:
        """
        화면 표시
        """
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        if light_recompute:
            light_map = initialize_light(game_map, fov_map, entities)
        render_all(game_state, root, console, panel, entities, player, mouse,
                   game_map, fov_map, light_map, camera, message_log, fov_recompute,
                   screen_width, screen_height,
                   bar_width, panel_height, panel_y, map_height, colors)
        context.present(root, keep_aspect=True, integer_scaling=True) # align=(0.5,1))
        #context.present(panel, keep_aspect=True, integer_scaling=True, align=(0.5,-1))

        clear_all_entities(console, entities, camera)

        fov_recompute = False
        light_recompute = False

        """
        입력에 대한 상호작용
        """

        action = handle_input_per_state(keyboard, mouse, context, game_state)
        #print(f'Mx:{mouse.x} My:{mouse.y} Clk:{mouse.click}')

        #Ridiculous failsafe
        if action == None:
            action = {}

        move = action.get('move')
        rest = action.get('rest')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        drop_inventory = action.get('drop_inventory')

        toggle_light  = action.get('toggle_light')
        create_luminary = action.get('create_light')
        toggle_wall  = action.get('toggle_wall')

        exit = action.get('exit')
        quit = action.get('quit')

        #print(action)
        player_turn_results = []

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                pass

        # 최대화면이 True일 시, 전체화면이 아니라면 콘솔을 전체화면으로 전환함
        if action.get('fullscreen'):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        """
        플레이어 차례에 플레이어가 할 수 있는 행동들
        """
        # move변수에 대입된 값이 있을 시 이동
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = action.get('move')
            destix = player.x + dx
            destiy = player.y + dy

            if debug.passwall == False:
                # 가려는 곳이 지형으로 안 막혀있으면
                if not game_map.is_blocked(destix, destiy):
                    # 거기에 이미 엔티티가 있나 확인
                    target = get_blocking_entities_at_location(entities, destix, destiy)

                    if target:
                        battle = target._Fighter

                        if battle:
                            attack_results = player._Fighter.attack(target)
                            player_turn_results.extend(attack_results)
                        else:
                            """
                            다음 층으로
                            """
                            if target._Portal:
                                entities = game_map.next_depth(player,message_log)
                                fov_map = initialize_fov(game_map)
                                fov_recompute = True
                                light_recompute = True
                                console.clear()
                            else:
                                print("This is the weirdest bug I've ever seen")

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
                message_log.log(Message(SYS_LOG['cannot_get_item'], tcod.yellow))

        if toggle_light:
            if player._Luminary.luminosity:
                player._Luminary.luminosity = 0
                fov_radius = 1
                fov_algorithm = fov_algorithm_dark
            else:
                player._Luminary.luminosity = player._Luminary.init_luminosity
                fov_radius = max_fov_radius
                fov_algorithm = fov_algorithm_lit

            fov_recompute = True
            light_recompute = True

            game_state = GameStates.ENEMY_TURN

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
                player_turn_results.extend(player._Inventory.use(item, camera=camera,
                                                                 entities=entities, fov_map=fov_map,
                                                                 screen_width = screen_width,
                                                                 screen_height = screen_height))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player._Inventory.drop_item(item))

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player._Inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        camera=camera, screen_width = screen_width, screen_height = screen_height,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if rest:
            game_state = GameStates.ENEMY_TURN

        for r in player_turn_results:
            message = r.get('message')
            dead_entity = r.get('dead')
            item_added = r.get('item_added')
            item_consumed = r.get('consumed')
            item_used = r.get('used')
            item_dropped = r.get('item_dropped')
            targeting = r.get('targeting')
            targeting_cancelled = r.get('targeting_cancelled')

            if message:
                message_log.log(message)

            if targeting_cancelled:
                game_state = previous_game_state
                message_log.log(Message('Targeting cancelled'))

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity, game_map)

                message_log.log(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed or item_used:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                message_log.log(targeting_item._Item.targeting_message)

        """
        적의 차례에 적이 할 수 있는 행동들
        """
        if game_state == GameStates.ENEMY_TURN:
            # 정신력 고갈 기능. 따로 변수로 넣던가 Gamemap에 넣어야 하나.
            if not game_map.monsters == 0:
                clear_message_shown = False

                sanity_damage = random.randint(int(-30/math.sqrt(game_map.depth)), game_map.monsters)
                if sanity_damage < 0:
                    sanity_damage = 0
                else:
                    sanity_damage = int(math.sqrt(sanity_damage))
                player._Fighter.heal_sanity(-sanity_damage)
                if sanity_damage > 3:
                    log = SYS_LOG['enemies_exist']
                    message_log.log(Message(log[random.randint(0,len(log)-1)],tcod.dark_chartreuse))
            else:
                if not clear_message_shown:
                    clear_message_shown = True
                    message_log.log(Message(SYS_LOG['enemies_nonexistant'],tcod.green))


            for entity in entities:
                if entity.name == 'light source':
                    pass
                    #message_log.log(f"The {entity.name} is glowing")
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
                                game_map.monsters -= 1

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

        if create_luminary:
            game_map.create_luminary(entities, player.x, player.y, 15)
            # 광원이 새로 생겼으니 다시 계산
            light_recompute = True


if __name__ == '__main__':
    main()