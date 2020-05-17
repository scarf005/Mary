class Rect:
    def __init__(self, x, y, w, h):
        """
        x,y 좌표를 받아 위치를 잡는다. w와 h는 각각 사각형의 너비와 높이를 결정한다.
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h