class Entity:
    """
    플레이어, 적, 아이템 등등 모든 것을 표현할 때 쓰는 객체.
    """
    def __init__(self, x, y, char, color):
        #엔티티 속성: x,y좌표, 외관(문자), 색깔
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # 엔티티를 지정한 양 만큼 이동시킴
        self.x += dx
        self.y += dy