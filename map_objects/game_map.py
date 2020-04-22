import tcod as libtcod

from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile

from components.luminary import Luminary

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
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        return tiles


    def make_map(self):
        pass

    def create_room(self, room):
        """
        주어진 사각형 객체의 내부를 움직일 수 있는 빈 공간(바닥)으로 채운다.
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

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

    """
    신규기능들
    """

    def toggle_wall(self,x,y):
        self.tiles[x][y].blocked ^= 1
        self.tiles[x][y].block_sight ^= 1


    def create_luminary(self, entities, x ,y):
        luminary_component = Luminary(luminosity=10)
        light = Entity(x, y, '&', libtcod.yellow, 'light source', blocks=False, luminary=luminary_component)
        entities.append(light)
