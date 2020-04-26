import random
import numpy as np

import time

def display(matrix):
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if matrix[y,x] == 1:
                char = "#"
            elif matrix[y,x] == 2:
                char = "$"
            else:
                char = "."
            print(char, end='')
        print()

def find_nook(wall_map, limit=5):
    """
    wall_map = 지도, 무조건 np.array 형식으로 받아야 할 것
    limit = 최소 인접한 벽의 수. 높을수록 드믐
    limit은 5나 6 정도가 적당함. 6이면 극히 드문 정도.
    """
    # 지금 numpy array는 shape, game_map은 그냥 array라서 충돌 일어남. 해결방법 찾을 것
    #print(wall_map)
    places = []
    for y in range (wall_map.shape[0]):
        for x in range (wall_map.shape[1]):
            if not wall_map[y,x]:
                if adjacent_walls(wall_map, x,y) >= limit:
                    # y,x 형식에 유의
                    places.append((y,x))
                
    return places

def adjacent_walls(wall_map, x,y):
    count = 0
    where = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for i in range(8):
        try:
            if wall_map[y+where[i][1],x+where[i][0]]:
                count +=1
        except:
            count +=1
    return count

def cell_auto(width, height, generation, init_chance = 0.5, birth_limit = 4, death_limit = 3):
    """
    generation = 반복 수
    init_chance = 벽 빈도
    """
    debug = False
    
    old_map = np.random.rand(height,width)
    old_map = np.where(old_map < init_chance, 1, 0)
    
    new_map = np.zeros((height,width),dtype='uint8')
    
    #TODO: Fill too small rooms. Apply flood fill.
    for gen in range(generation + 1):      
        old_map[old_map > 1] = 1
        new_map[:] = 0
        
        for y in range(height):
            for x in range(width):
                walls_1away = adjacent_walls(old_map, x,y)

                # 벽 주위에 이웃 벽들이 너무 적으면 파냄
                if old_map[y,x]:
                    if walls_1away < death_limit:
                        new_map[y,x] = 0
                    else:
                        new_map[y,x] = 1
                # 바닥 주위에 이웃 벽들이 많으면 채움
                else:
                    if walls_1away > birth_limit:
                        new_map[y,x] = 1
                    else:
                        new_map[y,x] = 0
        old_map[:] = 0
        old_map += new_map 
    return old_map

def make_cave(width, height, generation, init_chance, birth_limit = 4, death_limit = 3):
        while True:
            cave_map = cell_auto(width,height, generation, init_chance, birth_limit, death_limit)
            # 플레이어가 있는 위치가 빈 공간일 때 까지 생성
            if cave_map[int(height/2),int(width/2)] == 0:
                #가장자리 벽으로 둘러싸기
                cave_map[0,:] = 1
                cave_map[height-1,:] = 1
                cave_map[:,0] = 1
                cave_map[:,width-1] = 1
                return cave_map

if __name__ == '__main__':
    #start = input()
    print("\n"*2)
    new_map = make_cave(40, 40, 2, 0.4)
    treasures = find_nook(new_map)
    print (treasures)
    for i in range(len(treasures)):
        new_map[treasures[i][0],treasures[i][1]] = 2
    print("최종 결과")
    display(new_map)
    #print("\n"*2)
    
    quit = input()

