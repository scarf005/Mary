import tcod 
import numpy as np

from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile

from map_objects.map_generator.cellular_automata import cell_auto

from components.luminary import Luminary

class GameMap:
    def __init__(self, width, height):
        # 맵 크기 인자를 받아 객체의 높이와 너비 변수에 저장한다.
        self.width = width
        self.height = height

        """
        넘파이 연습중
        """
        self.tiles = self.initialize_tiles()


    def initialize_tiles(self):
        # 타일 리스트를 채운다. 타일(못지나감)을 채우는데, y에 대해 높이수만큼 쌓고, 그걸 또 너비수만큼 쌓는다.
        # 넘파이라서 y,x식으로 해야 함
        
        while True:
            wall_map = cell_auto(self.width,self.height, 6, 0.6)
            if wall_map[int(self.height/2),int(self.width/2)] == 0:
                break
        
        print (wall_map)
        wall_map = np.where(wall_map == 1 , Tile(True), Tile(False))
        return wall_map
        
        #np_tiles = np.array([[Tile(False) for x in range(self.width)] for y in range(self.height)])
        #return np_tiles


    def make_map(self):
        pass

    def create_room(self, room):
        """
        주어진 사각형 객체의 내부를 움직일 수 있는 빈 공간(바닥)으로 채운다.
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[y,x].blocked = False
                self.tiles[y,x].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        # x1 과 x2 사이 y
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y,x].blocked = False
            self.tiles[y,x].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        # 
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y,x].blocked = False
            self.tiles[y,x].block_sight = False

    def is_blocked(self, x, y):
        # 게임맵 객체의 tiles리스트에서 찾은 후 막혔는지 확인한다.
        # 에러뜨면 그냥 못지나간다고 값을 돌려준다.
        try:
            if self.tiles[y,x].blocked:
                return True
        except IndexError:
            return True

        return False

    """
    신규 기능들
    """

    def toggle_wall(self,x,y):
        self.tiles[y,x].blocked ^= 1
        self.tiles[y,x].block_sight ^= 1


    def create_luminary(self, entities, x ,y, brightness=5):
        luminary_component = Luminary(luminosity=brightness)
        light = Entity(x, y, '&', tcod.yellow, 'light source', blocks=False, luminary=luminary_component)
        entities.append(light)
