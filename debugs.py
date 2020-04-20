class Debug:
    """
    원판 강좌와는 관련이 없다. 불리언들은 붙여쓰고 함수들은 밑줄(_)로 써서 구별한다.
    인자에 원하는 기능을 집어넣으면 켜진다.
    """
    def __init__(self, *args):
        self.debug_prefix = "[Debug]"

        #기능들. 기본적으로는 꺼져 있다.
        self.passwall = False
        self.showpos = False

        #디버그 객체를 생성할 때 인자를 인자 형태로 받아서 수정할 수 있다.

        for i in args:
            if i in self.__dict__.keys():
                setattr(self, i, True)
            else:
                self.dbg_msg("You've put wrong parameter into the debug object. It's nullified but check it out later.")

    def dbg_msg(self, message):
        print (F"{self.debug_prefix} {message}")


    def show_pos(self, entity, name):
        #디버그: 플레이어 위치 표시
        self.dbg_msg(F"{name} x: {entity.x}, y: {entity.y}")

    
        
        
            