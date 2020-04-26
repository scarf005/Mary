def create_room(tiles, room):
        """
        주어진 사각형 객체의 내부를 움직일 수 있는 빈 공간(바닥)으로 채운다.
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tiles[y,x].blocked = False
                tiles[y,x].block_sight = False

def create_h_tunnel(tiles, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        tiles[y,x].blocked = False
        tiles[y,x].block_sight = False

def create_v_tunnel(tiles, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        tiles[y,x].blocked = False
        tiles[y,x].block_sight = False