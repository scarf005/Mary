import tcod as libtcod
from game_states import GameStates

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    #WASD
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    #Numpad
    elif key.vk == libtcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_KP6:
        return {'move': (1, 0)}

    #Numpad Diagonal
    elif key.vk == libtcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key.vk == libtcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key.vk == libtcod.KEY_KP3:
        return {'move': (1, 1)}
    elif key.vk == libtcod.KEY_KP1:
        return {'move': (-1, 1)}

    #Alt + Enter
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    #ESC
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    #[디버그] 벽 생성
    if key.vk == libtcod.KEY_1:
        return {'toggle_wall': True}

    #[디버그] 광원 생성
    if key.vk == libtcod.KEY_2:
        return {'create_luminary': True}

    #행동들
    if key_char ==  'q':
        return {'toggle_light': True}

    elif key_char == ',':
        return {'pickup': True}

    elif key_char == '.':
        return {'rest': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    #눌린 키가 없으면: 빈 값 반환
    return {}

def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}