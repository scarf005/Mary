import tcod as libtcod


def initialize_fov(game_map):
    """
    지도 객체를 받은 후 시야각을 처리한다
    """
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    # y, x 에 대해 반복
    for y in range(game_map.height):
        for x in range(game_map.width):
            #
            libtcod.map_set_properties(fov_map, x, y, 
                    not game_map.tiles[x][y].block_sight, not game_map.tiles[x][y].blocked)

    #계산한 시야각 결과를 반환
    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    #지도, 플레이어(또는 엔티티) 좌표, 시야 범위, 벽 밝히기 여부, 탐색 알고리즘
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)