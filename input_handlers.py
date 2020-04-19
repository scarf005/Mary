import tcod as libtcod

#사전 형식
def handle_keys(key):
    # 이동 키:상,하,좌,우 반환
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt 키와 Enter 키가 동시에 눌리면:전체화면 반환
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        #ESC 키가 눌리면: 종료 반환
        return {'exit': True}

    #눌린 키가 없으면: 빈 값 반환
    return {}