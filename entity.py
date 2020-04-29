import tcod
import math

from renderer.render_functions import RenderOrder

class Entity:
    """
    플레이어, 적, 아이템 등등 모든 것을 표현할 때 쓰는 객체.
    """
    def __init__(self, x, y, char, color, name, **kwargs):
        # 엔티티 속성: x,y좌표, 외관(문자), 색깔
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color

        # 기타 속성들
        component_list = {'blocks':False, 'render_order':RenderOrder.CORPSE,
                          '_Luminary':None, '_Fighter':None, '_Ai':None,
                          '_Item':None, '_Inventory':None}
        for key,value in component_list.items():
            #print("kwargs")
            #print (kwargs)
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                setattr(self, key, value)

        # 컴포넌트 소유주 추가
        if self._Luminary:
            self._Luminary.owner = self

        if self._Fighter:
            self._Fighter.owner = self

        if self._Ai:
            self._Ai.owner = self

        if self._Item:
            self._Item.owner = self

        if self._Inventory:
            self._Inventory.owner = self

    def distance_to(self, other):
            dx = other.x - self.x
            dy = other.y - self.y
            return math.sqrt(dx ** 2 + dy ** 2)

    def move(self, dx, dy):
        #  엔티티를 지정한 양 만큼 이동시킴
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                    get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov_map = tcod.map.Map(width=game_map.width, height=game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                fov_map.transparent[y1,x1] = not game_map.tiles[y1,x1].block_sight
                fov_map.walkable[y1,x1] = not game_map.tiles[y1,x1].blocked

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                fov_map.transparent[entity.y,entity.x] = True
                fov_map.walkable[entity.y,entity.x] = False

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov_map, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)


"""
클래스 밖 함수
"""

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None

