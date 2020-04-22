class Luminary:
    """
    광원 객체. 광원 객체들은 밝기만큼 지도를 밝히고, game_map.tiles[y,x]에 밝기 값을 저장한다
    """
    def __init__(self, luminosity):
        self.luminosity = luminosity

    def explain(self):
        print(F"this luminary object is as bright as {self.luminosity}... something.")