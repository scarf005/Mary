import random
import numpy as np

import time

def display(matrix):
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            char = "#" if matrix[y,x] == 1 else "."
            print(char, end='')
        print()

def make_cave(width, height, generation, init_chance, birth_limit = 4, death_limit = 3):
        while True:
            cave_map = cell_auto(width,height, generation, init_chance, birth_limit, death_limit)
            # 플레이어가 있는 위치가 빈 공간일 때 까지 생성
            if cave_map[int(height/2),int(width/2)] == 0:
                return cave_map

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
    cell_map = np.random.rand(height,width)
    cell_map = np.where(cell_map < init_chance, 1, 0)

    #TODO: change alive_neighbors counting mechanism so it doesn't break. Maybe add new func.
    #TODO: Fill too small rooms. Apply flood fill.
    for gen in range(generation + 1):
        #print(F"{gen}번째 반복")
        #display(cell_map)
        new_map = np.zeros((height,width),dtype='uint8')
        for y in range(height):
            for x in range(width):
                #alive_neighbors = cell_map[max(y-1, 0):min(y+2, height),max(x-1, 0):min(x+2, width)]
                #walls_1away = len(np.where(alive_neighbors.flatten() == 1)[0])
                walls_1away = adjacent_walls(cell_map, x,y)

                if cell_map[y,x]:
                    if walls_1away < death_limit:
                        new_map[y,x] = 0
                    else:
                        new_map[y,x] = 1

                else:
                    if walls_1away > birth_limit:
                        new_map[y,x] = 1
                    else:
                        new_map[y,x] = 0
        cell_map += new_map 
        #print("\n\n")
        #time.sleep(0.8)
        
    
    #가장자리 벽으로 둘러싸기
    cell_map[0,:] = 1
    cell_map[height-1,:] = 1
    cell_map[:,0] = 1
    cell_map[:,width-1] = 1
    return cell_map


if __name__ == '__main__':
    #start = input()
    print("\n"*2)
    new_map = cell_auto(25, 20, 2, 0.4)
    print("최종 결과")
    display(new_map)
    #print("\n"*2)
    
    quit = input()

