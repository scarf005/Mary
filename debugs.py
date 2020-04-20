class Debug:
    def __init__(self):
        pass

    def show_pos(self,entity,name):
        #디버그: 플레이어 위치 표시
        print(F"{name} x: {entity.x}, y: {entity.y}")
            