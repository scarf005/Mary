import tcod as libtcod
import numpy as np

def initialize_fov(game_map):
    fov_map = libtcod.map.Map(width=game_map.width, height=game_map.height)
    #넘파이 리스트들은 (y,x) 형식
    #[1:3]은 range처럼 1,2 를 의미하는 것 유의
    for y in range(game_map.height):
        for x in range(game_map.width):
            fov_map.transparent[y,x] = not game_map.tiles[y,x].block_sight #working
            fov_map.walkable[y,x] = not game_map.tiles[y,x].blocked
    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    #print(F"transparent:{fov_map.transparent},walkable:{fov_map.walkable}")
    #투명도: np.ndarray, 위치: Tuple[int, int]
    fov_map.compute_fov(x,y, radius, light_walls, algorithm)