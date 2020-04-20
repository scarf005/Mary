from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        #맵 크기 인자를 받아 객체의 높이와 너비 변수에 저장한다.
        self.width = width
        self.height = height

        """
        새로운 GameMap 객체가 생성되면 init_tiles() 함수를 실행한다.
        실행하면 게임 화면 크기만큼 타일 객체가 생성되며,
        이 객체들을 GameMap 객체의 tiles 리스트에 대입한다.
        """
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        #타일 리스트를 채운다. 타일(못지나감)을 채우는데, y에 대해 높이수만큼 쌓고, 그걸 또 너비수만큼 쌓는다.
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles


    def make_map(self):
        # Create two rooms for demonstration purposes
        room1 = Rect(1, 1, 5, 5)
        room2 = Rect(12, 12, 4, 4)

        self.create_room(room1)
        self.create_room(room2)

    def create_room(self, room):
        """
        주어진 사각형 객체의 내부를 움직일 수 있는 빈 공간(바닥)으로 채운다.
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        """
        어째서 x.1과 y.1에 1을 더할까? 외벽의 두께를 2칸으로 해서, 
        방 두개를 바로 맡붙여놓아도 둘이 합쳐지지 않게 하기 위해서다.
        그런데 x.2와 y.2에는 1을 빼지 않는다. 그 이유는 range(a,b)함수가
        마지막, 즉 b번째 수는 세지 않기 때문이다. 즉 이미 빠져 있다는 것.
        파이썬의 자료구조는 (+대부분의 언어에서는) 셈을 0부터 시작하기 때문이다.
        가령 range(1,5) -> [1,2,3,4] (총 4개) 이런 식이다.

        예시)
        (1,1) 에서 (6,6) 사이에 빈 공간을 만든다고 할 때,
        다른 방이랑 겹치지 않으려면 % 부분은 채워져있어야 한다.

          0 1 2 3 4 5 6 7
        0 # # # # # # # #
        1 # % % % % % % #
        2 # % . . . . % #
        3 # % . . . . % #
        4 # % . . . . % #
        5 # % . . . . % #
        6 # % % % % % % #
        7 # # # # # # # #

        (1,1) 부터 (6,6) 까지 지정하려면 Rect는 (1,1,5,5)가 될 것이다.
        range(1,5)는 상술했듯 [1,2,3,4] 4개. 4x4 공간만 뚫리게 된다.
        (x2는 x1 + w 이니 1 + 5 = 6. 그런데 강좌에선 이렇게 했는데 좀 더 직관적으로 하려면
        self.x2는 x + w 가 아니라 x + w - 1 이 되어야 할 것이다. 
        그런데 이렇게 하면 맵 생성 시 어떻게 될 지 모르니 다음에 확인해보겠음.
        """

    def create_h_tunnel(self, x1, x2, y):
        #x1 과 x2 사이 y
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        #
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        #게임맵 객체의 tiles리스트에서 찾은 후 막혔는지 확인한다.
        #에러뜨면 그냥 못지나간다고 값을 돌려준다.
        try:
            if self.tiles[x][y].blocked:
                return True
        except IndexError:
            return True

        return False
