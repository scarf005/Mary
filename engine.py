import tcod as libtcod
import numpy as np

from entity import Entity
from input_handlers import handle_keys

from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from fov_functions import initialize_fov, recompute_fov

from debugs import Debug

#메인 루프
def main():
    #스크린 가로/세로 크기
    screen_width = 40
    screen_height = 25

    #지도
    map_width = 30
    map_height = 20

    #FOV
    fov_algorithm = 2
    fov_light_walls = True
    fov_radius = 12

    #타일 색깔
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50),
        'pitch_black': libtcod.Color(0,0,0,)
    }

    """
    객체 생성
    """
    #플레이어 객체 생성. 위치는 맵 중앙.
    player = Entity(int(map_width/2),int(map_height/2),'@',libtcod.white, 'player')
    entities = [player]

    #지도 객체 생성
    game_map = GameMap(map_width, map_height)

    #FOV
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    """
    디버그 명령 목록
    passwall: 벽 통과 가능
    showpos: 플레이어 x,y좌표 표시. 다른 엔티티 좌표도 표시할 수 있게 고칠 것
    """
    #디버그용 객체 생성. 디버그 기능들은 기본적으로 꺼져 있고, 인자를 넣으면 활성화
    debug = Debug()

    
    #키보드, 마우스 입력 처리용 객체 생성
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    #콘솔 con 생성
    con = libtcod.console_new(screen_width, screen_height)



    #폰트 설정: 10x10파일, 이미지 파일은 그레이스케일, 배열 방식은 TCOD
    #libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #폰트 설정: 32x32파일, 이미지 파일은 그레이스케일, 배열 방식은 CP437
    libtcod.console_set_custom_font('terminal32x32.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)

    #스크린 생성: 스크린 가로/세로, 이름, 전체화면 여부
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    

    #TCOD 루프
    while not libtcod.console_is_window_closed():
        """
        입력
        """
        #사용자 입력을 받음: 키 누를 시, 키보드, 마우스
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        """
        화면 표시
        """
        #fov
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        #표시할 모든 객체를 화면에 배치함
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        #화면 출력
        libtcod.console_flush()

        #화면 초기화
        clear_all(con, entities)

        """
        입력에 대한 상호작용
        """
        #action 변수에 키보드 입력값을 사전 형태로 받아옴
        action = handle_keys(key)

        #action 변수에 입력한 키워드에 대응한 값을 move 변수에 대입
        move = action.get('move') 
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #move변수에 대입된 값이 있을 시 이동
        if move:
            dx, dy = move
            if debug.passwall == False:
                if not game_map.is_blocked(player.x + dx, player.y + dy):
                    player.move(dx, dy)

                    fov_recompute = True
            else:
                if game_map.is_blocked(player.x + dx, player.y + dy):
                    debug.dbg_msg("You magically pass through solid wall.")
                player.move(dx, dy)

        #최대화면이 True일 시, 전체화면이 아니라면 콘솔을 전체화면으로 전환함
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        """
        기타
        """

        #플레이어 위치 표시
        if debug.showpos: debug.show_pos(player,'player')

        #벽 설치
        toggle_wall = action.get('toggle_wall')

        #광원 설치
        create_luminary = action.get('create_luminary')

        if toggle_wall:
            game_map.toggle_wall(player.x, player.y)
            #지형이 변했으니 새로 지형 맵을 짜야 함
            fov_map = initialize_fov(game_map)
            print (fov_map)
        
        if create_luminary:
            game_map.create_luminary(entities, player.x, player.y)



if __name__ == '__main__':
    main()