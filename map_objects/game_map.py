from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        #맵 크기 인자를 받아 객체의 높이와 너비 변수에 저장한다.
        self.width = width
        self.height = height

        """
        새로운 GameMap 객체가 생성되면 init_tiles() 함수를 실행한다.
        실행하면 게임 화면 크기만큼 타일 객체가 생성되며,
        이 객체들을 GameMap 객체의 tiles 리스트에 대입한다.
        """
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        #타일 리스트를 채운다. 타일(시야막음)을 채우는데, y에 대해 높이수만큼 쌓고, 그걸 또 너비수만큼 쌓는다.
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        #테스트용으로 일정 위치에 벽들을 설치함. 3강부터 지워질 것.
        tiles[10][12].blocked = True
        tiles[10][12].block_sight = True
        tiles[11][12].blocked = True
        tiles[11][12].block_sight = True
        tiles[12][12].blocked = True
        tiles[12][12].block_sight = True

        return tiles

    def is_blocked(self, x, y):
        """
        try-catch 구문은 원본 튜토리얼에 없는 내용. 벽으로 가면 에러 뜨길레 우회용으로 추가함. 
        이건 아직 지형이 구현 안 되서 생기는 오류로, 3강에서 맵 구현이 되면 화면 가장자리에 갈 일이 원천봉쇄되기
        때문에 사실 의미없는 짓이다.
        """
        try:
            if self.tiles[x][y].blocked:
                return True
        except IndexError:
            return True

        return False