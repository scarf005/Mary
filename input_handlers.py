import tcod as libtcod

#사전 형식
def handle_keys(key):
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

    #벽 생성
    if key.vk == libtcod.KEY_1:
        return {'toggle_wall': True}

    #광원 생성
    if key.vk == libtcod.KEY_2:
        return {'create_luminary': True}
    
    #전등 토글
    if key_char ==  'q':
        return {'toggle_light': True}

    #눌린 키가 없으면: 빈 값 반환
    return {}