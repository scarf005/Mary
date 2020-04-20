class Rect:
    def __init__(self, x, y, w, h):
        """
        x,y 좌표를 받아 위치를 잡는다. w와 h는 각각 사각형의 너비와 높이를 결정한다.
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        #중심을 구한다.
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        #만약에 자기(self)가 다른 직사각형(other)과 겹친다면 True를 반환한다.
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)