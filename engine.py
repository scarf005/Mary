import tcod as libtcod
from input_handlers import handle_keys

#메인 루프
def main():
    #스크린 가로/세로 크기
    screen_width = 40
    screen_height = 25

    #플레이어 좌표는 화면 정가운데
    player_x = int(screen_width/2)
    player_y = int(screen_height/2)


    #폰트 설정: 10x10파일, 이미지 파일은 그레이스케일, 배열 방식은 TCOD
    #libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #폰트 설정: 32x32파일, 이미지 파일은 그레이스케일, 배열 방식은 CP437
    libtcod.console_set_custom_font('terminal32x32.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)

    #스크린 생성: 스크린 가로/세로, 이름, 전체화면 여부
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    #콘솔 con 생성
    con = libtcod.console_new(screen_width, screen_height)
    
    #키보드, 마우스 입력
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    #디버그용 변수
    frame = 0

    #TCOD 루프
    while not libtcod.console_is_window_closed():
        #사용자 입력을 받음: 키 누를 시, 키보드, 마우스
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        #기본 글자색:'con' 콘솔, 색깔:하얀색
        libtcod.console_set_default_foreground(con, libtcod.white) 
        #기호 출력: 'con' 콘솔, x,y좌표, @기호, 배경색:없음 
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE) 
        
        #변화 내용 갱신
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        #화면 출력
        libtcod.console_flush()

        #기호 출력: 'con' 콘솔, x,y좌표, 기호 없음, 배경색:없음 
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE) 

        #디버그: 플레이어 위치 표시
        frame += 1
        if frame % 6 == 0:
            print(F"player x: {player_x}, y: {player_y}")
            frame = 0

        #action 변수에 키보드 입력값을 사전 형태로 받아옴
        action = handle_keys(key)

        #action 변수에 입력한 키워드에 대응한 값을 move 변수에 대입
        move = action.get('move') 
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #move변수에 대입된 값이 있을 시 이동
        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        #최대화면이 True일 시, 전체화면이 아니라면 콘솔을 전체화면으로 전환
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()