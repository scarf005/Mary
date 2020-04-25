import tcod 
import numpy as np

def initialize_light(game_map, fov_map, entities):
    """
    광원 위치 결정: light_map (0은 광원, 999는 벽)
    막힌 곳 표시: cost (0: 막힘 1: 빈 공간)
    시야 막힌것 표시할 때: fov_map
    """
    # cardinal, diagonal: 상하좌우 / 대각선 이동시 비용. 1.4로 하면 대각선 거리 반영됨

    # 너비, 높이 일괄 변수
    W = game_map.width
    H = game_map.height

    """
    광원 위치 지도 생성
    """
    # 광원 위치 결정용 light_map 생성. 
    # [넘파이 array, 높이:H 너비:W 채울 값(full):999]
    light_map = np.full((H,W),999)

    # 광원 엔티티 생성
    for E in entities:
        try:
            if E.luminary.luminosity:
                light_map[E.y, E.x] = -E.luminary.luminosity
        except:
            pass

    # 막힌 곳 표시용 cost 생성, 1은 빈 공간 0은 막힌 공간. 즉 숫자는 가는데 걸리는 시간
    # cost는 안 변함. light_map이 변하는 것.

    """
    벽 지도 생성
    """
    # 처음 전부 뚫린 지도 생성
    cost = np.ones((H,W), dtype=np.uint8)

    """
    코드 너무 난잡함. 나중에 수정할 것
    """
    # fov_map.walkable 은 bool array, cost는 전부 1이니까 walkable = False 면 -= False니까 +1
    unwalkable = 1 - fov_map.walkable
    unwalkable = unwalkable.astype('uint8')
    cost -= unwalkable

    # 디악스트라 거리 계산
    tcod.path.dijkstra2d(light_map,cost,1,1)

    #print(F"Cost: \n {cost} \n Light map: \n{light_map}"

    return light_map


def mix_rgb(color,brightness):
    color_setting = -(brightness * 10 **0.5)
    C = np.array(list(color))
    L = np.array([int((color_setting)/ ((i+1)**0.5)) for i in range(3)])
    T = C + L - 30
    #값이 8비트를 초과하면 오버플로우 막기
    T[T>255] = 255
    T[T<0] = 0
    return tuple(T)