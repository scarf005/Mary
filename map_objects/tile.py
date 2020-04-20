class Tile:
    """
    지도에 표시되는 타일. 움직임 또는 시야를 막거나 막지 않을 수 있다.
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        
        #기본적으로 타일이 통과 불가능하다면 불투명하다.
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight