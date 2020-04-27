import tcod 
import numpy as np
from random import randint

from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile

from map_objects.map_generator.cellular_automata import make_cave, find_nook

from components.luminary import Luminary

class GameMap:
    def __init__(self, width, height):
        # 맵 크기 인자를 받아 객체의 높이와 너비 변수에 저장한다.
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        

    def initialize_tiles(self):                  
        return np.array([[Tile(True) for x in range(self.width)] for y in range(self.height)])
        
    def create_map_cave(self, entities, min_nook, max_entities):
        while True:
            wall_map = make_cave(self.width, self.height, 3, 0.4)  
            if len(find_nook(wall_map)) >= min_nook: break

        for y in range(self.height):
            for x in range(self.width):
                if not wall_map[y,x]:
                    self.tiles[y,x].blocked = False
                    self.tiles[y,x].block_sight = False
        self.place_entities_at_nook(entities, min_nook, max_entities)
    
    def place_entities_at_nook(self, entities, min_monsters, max_monsters):      
        wall_map = np.zeros((self.height,self.width),dtype='uint8')    
    
        for y in range(self.height):
            for x in range(self.width):
                wall_map[y,x] = 1 if self.tiles[y,x].blocked else 0
                
        nooks = find_nook(wall_map)
        monster_num = randint(min_monsters, max_monsters)
        
        if len(nooks) < monster_num:
            monster_num = len(nooks)
        
        for i in range(monster_num):
            if randint(0, 100) < 80:
                monster = Entity(nooks[i][1], nooks[i][0], '~', tcod.flame, 'crawling intestines', blocks=True)
            else:
                monster = Entity(nooks[i][1], nooks[i][0], 'S', tcod.dark_green, 'giant spider', blocks=True)
            entities.append(monster)
        
        # 남는 공간이 있으면 램프 생성
        if not len(nooks) - monster_num == 0:
            for i in range(len(nooks) - monster_num):
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
        light = Entity(x, y, '&', tcod.yellow, 'light source',_Luminary=luminary_component)
        entities.append(light)