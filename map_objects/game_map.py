import tcod 
import numpy as np
from random import randint

from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile

from map_objects.map_generator.cellular_automata import make_cave, find_nook

from components.luminary import Luminary

class GameMap:
    def __init__(self, width, height, entities):
        # 맵 크기 인자를 받아 객체의 높이와 너비 변수에 저장한다.
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles(entities)

    def initialize_tiles(self, entities):       
        #원래는 이걸 하고 싶었는데.
        #wall_map = np.where(wall_map == 1 , Tile(True), Tile(False))                   
        np_tiles = np.array([[Tile(True) for x in range(self.width)] for y in range(self.height)])
        wall_map = make_cave(self.width, self.height, 3, 0.4)        
        """
        지금은 임시로 구석진 곳에 램프를 설치함
        """    
        self.place_lamp_at_nook(wall_map,entities)
        
        for y in range(self.height):
            for x in range(self.width):
                if not wall_map[y,x]:
                    np_tiles[y,x].blocked = False
                    np_tiles[y,x].block_sight = False
        return np_tiles
    
    def place_lamp_at_nook(self, wall_map, entities):       
        nooks = find_nook(wall_map)
        for i in range(len(nooks)):
            self.create_luminary(entities, nooks[i][1], nooks[i][0], 15)
        

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
    디버그 기능들
    """

    def toggle_wall(self,x,y):
        self.tiles[y,x].blocked ^= 1
        self.tiles[y,x].block_sight ^= 1

    def create_luminary(self, entities, x ,y, brightness=5):
        luminary_component = Luminary(luminosity=brightness)
        light = Entity(x, y, '&', tcod.yellow, 'light source', blocks=False, luminary=luminary_component)
        entities.append(light)