import random
import numpy as np

def display(matrix):
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            char = "#" if matrix[y,x] == 1 else "."
            print(char, end='')
        print()

def cell_auto(width, height, generation, init_chance = 0.5, birth_limit = 4, death_limit = 3):
    """
    generation = 반복 수
    init_chance = 벽 빈도
    """

    cell_map = np.random.rand(height,width)
    cell_map = np.where(cell_map < init_chance, 1, 0)

    for gen in range(generation + 1):
        for y in range(height):
            for x in range(width):
                # 1칸 떨어진 벽들 수를 구함
                submap = cell_map[max(y-1, 0):min(y+2, height),max(x-1, 0):min(x+2, width)]
                walls_1away = len(np.where(submap.flatten() == 1)[0])
                # 2칸 떨어진 벽들 수를 구함
                submap = cell_map[max(y-2, 0):min(y+3, height),max(x-2, 0):min(x+3, width)]
                walls_2away = len(np.where(submap.flatten() == 1)[0])
                # 벽 굳히기
                # for first five generations build a scaffolding of walls
                if gen < generation:
                    """
                    1칸 거리에서 5개 이상 벽이 보이면 벽 생성, 아니라면
                    2칸 거리에서 7개 이하 벽이 보이면 벽 생성
                    """
                    if walls_1away >= 5 or walls_2away <= 7:
                        cell_map[y,x] = 1
                    else:
                        cell_map[y,x] = 0
                    """
                    빈공간을 만들고 동떨어진 벽 비우기.
                    마지막 반복에서 걷는 거리를 늘림.
                    """
                else:
                    # 마지막 순서에서, 1칸 거리에 벽이 5개 이상이면 벽
                    if walls_1away >= 5:
                        cell_map[y,x] = 1
                    else:
                        cell_map[y,x] = 0
    
    #가장자리 벽으로 둘러싸기
    cell_map[0,:width] = 1
    cell_map[height - 1,:width] = 1
    cell_map[:height - 1,0] = 1
    cell_map[:height - 1,width - 1] = 1
    return cell_map


if __name__ == '__main__':
    new_map = cell_auto(25, 20, 3, 0.3)
    display(new_map)
