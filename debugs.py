class Debug:
    """
    원판 강좌와는 관련이 없다. 이것저것 테스트할때 쓰려고 만든 건데 자세한 건 나도 몰러.
    불리언들은 붙여쓰고 함수들은 밑줄(_)로 써서 구별한다.
    """
    def __init__(self, **kwargs):
        self.passwall = False
        self.showpos = False

        #디버그 객체를 생성할 때 인자를 사전 형태로 받아서 수정할 수 있다. 자세한 건 나도 몰라.
        #모르는 걸 다루면 패가망신이라고 했건만 일단은 다음에 걱정해야겠다.
        self.__dict__.update(kwargs)

    def show_pos(self,entity,name):
        #디버그: 플레이어 위치 표시
        print(F"{name} x: {entity.x}, y: {entity.y}")
        
        
            