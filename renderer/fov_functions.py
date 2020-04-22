import tcod 
import numpy as np

def initialize_fov(game_map):
    fov_map = tcod.map.Map(width=game_map.width, height=game_map.height)
    #game_map 에서 필요한 정보들을 fov_map으로 넘긴다
    for y in range(game_map.height):
        for x in range(game_map.width):
            fov_map.transparent[y,x] = not game_map.tiles[y,x].block_sight #working
            fov_map.walkable[y,x] = not game_map.tiles[y,x].blocked
    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    #print(F"transparent:{fov_map.transparent},walkable:{fov_map.walkable}")
    #투명도: np.ndarray, 위치: Tuple[int, int]
    fov_map.compute_fov(x,y, radius, light_walls, algorithm)
    print (fov_map.fov)