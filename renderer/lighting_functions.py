import tcod 
import numpy as np

def compute_light(fov_map, x,y, luminosity):
    """
    luminosity: 광원 관련
    brightness: 밝아지는 것들 관련
    """
    print(F"{fov_map.shape}")

def calculate_max_radius(luminosity):
    #밝기가 10 이하일 때까지 거리를 늘림. 아마 안 쓸 것. 다익스트라 방법으로 구현예정
    r=1
    brightness = luminosity
    while brightness >= 10:
        print (F"{r},{brightness}")
        brightness = round(luminosity / (r**2))
        r += 1
    return r - 1
