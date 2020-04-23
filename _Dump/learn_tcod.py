import tcod
import numpy as np


"""
필요한 것들: 
시야 막힌것 표시할 때 쓸 fov_map
막힌 곳을 표시할 때 필요한 cost
광원 위치를 결정하는 distance = light_map
"""

# 넘파이 객체들은 y,x인거 잊지 말자
fovMap = tcod.map.Map(8,8)
fovMap.transparent[:] = True
fovMap.transparent[6:8, :7] = False
print (fovMap.transparent)


"""
다익스트라 밝기 구현법:
cost: 지도, 0이 막힌 곳
"""
cost = np.zeros((8, 8), dtype=np.uint8)
cost[:3, 1] = 0
cost[3, 1:4] = 0
cost[2,4] = 0


for y in range(fovMap.transparent.shape[0]):
    for x in range(fovMap.transparent.shape[1]):
        if not fovMap.transparent[y,x]:
            cost [y,x] = 0
    

distance1 = np.full((8,8),999)
distance1[0,5] = 0
distance1[5,1] = 0

print(distance1)


tcod.path.dijkstra2d(distance1,cost,1,1)

print(F"cost:\n{cost} \n dist:\n{distance1}")
