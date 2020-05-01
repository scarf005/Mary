import tcod
import math
import numpy as np
from random import randint, shuffle

from game_messages import Message
from yaml_data.yaml_loader import open_yaml

# 지도
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from map_objects.map_generator.cellular_automata import make_cave, find_caverns, find_nook

# 엔티티, 컴포넌트
from entity import Entity
from item_functions import heal, read, talisman, cast_spell, cast_fireball

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.luminary import Luminary
from components.portals import Portal

# 렌더링
from renderer.render_functions import RenderOrder

class GameMap:
    def __init__(self, width, height, depth=1):
        # 맵 크기 인자를 받아 객체의 높이와 너비 변수에 저장한다.
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.depth = depth

    def initialize_tiles(self):
        return np.array([[Tile(True) for x in range(self.width)] for y in range(self.height)])

    def create_map_cave(self, player, entities, min_nook, max_monsters, max_items):
        """
        min_nook: 지도에서 구석진 곳의 최소 수 (아이템/몬스터 설치)
        max_monsters, max_items: 더 이상의 자세한 설명은 생략한다.
        """
        while True:
            wall_map = make_cave(player, self.width, self.height, 2, 0.4)
            if len(find_nook(wall_map)) >= min_nook and find_caverns(wall_map)[0] == 1: break

        for y in range(self.height):
            for x in range(self.width):
                if not wall_map[y,x]:
                    self.tiles[y,x].blocked = False
                    self.tiles[y,x].block_sight = False

        self.place_entities_at_nook(entities, min_nook, max_monsters, max_items)

    def next_depth(self, player, message_log):
        self.depth += 1
        entities = [player]

        #placeholder vars
        min_nook = 3
        max_monster, max_items = 10, 10

        self.tiles = self.initialize_tiles()
        self.create_map_cave(player, entities, min_nook, max_monster, max_items)
        player._Fighter.heal_sanity_capacity(player._Fighter.max_sanity // 2)
        self.create_portal(entities, 10, player)

        message_log.log(Message('You jump into the tear in the fabric of timespace.', tcod.light_violet))
        return entities

    def create_portal(self, entities, min_distance, player):
        """
        다음 층으로 가는 포탈 생성.
        min_distance:플레이어로부터 떨어져야 하는 최소 거리
        """
        x, y, dist = 0, 0, 0
        while dist < min_distance or self.tiles[y,x].blocked:
            x = randint(0, self.width-1)
            y = randint(0, self.height-1)
            dist = math.sqrt((x - player.x)**2 + (y - player.y)**2)

        portal_comp = Portal(self.depth + 1)
        down_portal = Entity(x, y, 'O', tcod.light_purple, 'Gap',
                             render_order=RenderOrder.PORTAL, blocks=True,
                             _Portal=portal_comp, _Luminary=Luminary(luminosity=20))
        entities.append(down_portal)

    def place_entities_at_nook(self, entities, min_monsters, max_monsters, max_items):
        # 벽 지도 생성
        wall_map = np.zeros((self.height,self.width),dtype='uint8')
        for y in range(self.height):
            for x in range(self.width):
                wall_map[y,x] = 1 if self.tiles[y,x].blocked else 0

        # 구석 개수 설정
        nooks = find_nook(wall_map)
        monster_num = randint(min_monsters, max_monsters)

        # 몬스터 배치
        Tm = 0
        for j in range(monster_num):
            if j < len(nooks):
                mx = nooks[j][1]
                my = nooks[j][0]
            else:
                # 구석진 곳이 모자르면 지도에서 무작위로 좌표를 뽑아옴
                my, mx = self.np_find_empty_cell(entities, wall_map)

            ai_comp = BasicMonster()
            monster_chance = randint(0, 100)

            if monster_chance < 60:
                f_comp = Fighter(hp=10, defense=0, power=3)
                monster = self.create_monster(mx,my, '~', tcod.flame, 'crawling intestine',
                                            f_comp, ai_comp)
            elif monster_chance < 90:
                f_comp = Fighter(hp=16, defense=1, power=4)
                monster = self.create_monster(mx,my, 'S', tcod.dark_green, 'giant spider',
                                            f_comp, ai_comp)
            else:
                f_comp = Fighter(hp=20, defense=0, power=7)
                monster = self.create_monster(mx,my, '@', tcod.Color(128, 5, 5),
                                              'flesh abomination',
                                              f_comp, ai_comp)
            entities.append(monster)
            Tm +=1
        print(F"monsters {Tm}")

        # 아이템 배치, 아직 임시
        i_nooks = nooks
        shuffle(i_nooks)
        if max_items > len(i_nooks):
            max_items = len(i_nooks)

        for i in range(len(i_nooks)):
            ix = i_nooks[i][1]
            iy = i_nooks[i][0]

            kinds = randint(1,4)
            if kinds == 1:
                i_comp = Item(use_function=heal, amount=10)
                item = self.create_item(ix, iy, '!', tcod.violet, 'Potion of Regeneration',item=i_comp)
            elif kinds == 2:
                i_comp = Item(use_function=heal, amount=2)
                item = self.create_item(ix, iy, '!', tcod.orange, 'Fruit Juice',item=i_comp)
            elif kinds == 3:
                i_comp = Item(use_function=cast_spell, damage=(1,20), maximum_range=5)
                item = self.create_item(ix, iy, '?', tcod.green, 'Manuscript of Spell Card',item=i_comp)
            elif kinds == 4:
                i_comp = Item(use_function=cast_fireball, targeting=True,
                              targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', tcod.light_cyan),
                              damage=(3,8,5), radius=3)
                item = self.create_item(ix, iy, '?', tcod.red, 'Manuscript of Hurl Fireball',item=i_comp)
            entities.append(item)

        """
        # 남는 공간이 있으면 램프 생성
        if not len(nooks) - monster_num == 0:
            for i in range(monster_num+1,len(nooks) - monster_num):
                self.create_luminary(entities, mx, my, 15)
        """

    def create_monster(self, x, y, char, color, name, fighter, ai):
        return Entity(x,y, char, color, name, blocks=True,
                      render_order=RenderOrder.ACTOR, _Fighter=fighter, _Ai=ai)

    def create_item(self, x, y, char, color, name, item):
        return Entity(x,y, char, color, name, render_order=RenderOrder.ITEM, _Item=item)

    def np_find_empty_cell(self, entities, game_map):
        while True:
            y,x = game_map[randint(0,game_map.shape[0]),randint(0,game_map.shape[1])]
            if game_map[y,x] == 0:
                for i in entities:
                    if y == i.y and x == i.x:
                        break
                else:
                    return y,x

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