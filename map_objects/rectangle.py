class Rect:
    def __init__(self, x, y, w, h):
        """
        x,y 좌표를 받아 위치를 잡는다. w와 h는 각각 사각형의 너비와 높이를 결정한다.
        """
        # x1 = 0, w = 3 이라고 하면 x2 는 2가 된다. 0, 1, 2 총 3칸.
        # 때문에 x2는 현재 좌표에 (너비 - 1) 만큼을 더한 값이 된다.
        self.x1 = x
        self.y1 = y
        self.x2 = x + w - 1
        self.y2 = y + h - 1

    def center(self):
        # 중심을 구한다.
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        """
        이 사각형 x1이 다른 사각형 x2보다 같거나 작고, 이 사각형 x2가 다른 사각형 x1보다 같거나 크고,
        y에 대해서도 같다면 True를 반환한다. 즉 겹친다고 판단한다.
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

        #만약에 True가 나오는 상황이라면 self.x1 <= other.x1 <= self.x2 <= self.x2 일 것이다.
        #만약에 둘의 y좌표가 겹치지 않는다면 겹치는 것이 아니기 때문에, x와 y의 좌표 둘다 동시에 겹침을 만족해야 한다.
        #겹치지 않으려면 self.x2 < other.x1 이어야 할 것이다.
        
