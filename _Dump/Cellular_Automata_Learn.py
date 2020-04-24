import random
import numpy as np

def display_cave(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            char = "#" if matrix[i][j] == WALL else "."
            print(char, end='')
        print()

# the cave size
shape = (15,30)

# walls will be 0
# floors will be 1
WALL = 0
FLOOR = 1
fill_prob = 0.25

new_map = np.ones(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        choice = random.uniform(0, 1)
        new_map[i][j] = WALL if choice < fill_prob else FLOOR

# run for given generations
generations = 5
for generation in range(generations):
    for i in range(shape[0]):
        for j in range(shape[1]):
            # get the number of walls 1 away from each index
            # get the number of walls 2 away from each index
            submap = new_map[max(i-1, 0):min(i+2, new_map.shape[0]),max(j-1, 0):min(j+2, new_map.shape[1])]
            wallcount_1away = len(np.where(submap.flatten() == WALL)[0])
            submap = new_map[max(i-2, 0):min(i+3, new_map.shape[0]),max(j-2, 0):min(j+3, new_map.shape[1])]
            wallcount_2away = len(np.where(submap.flatten() == WALL)[0])
            # this consolidates walls
            # for first five generations build a scaffolding of walls
            if generation < 5:
                # if looking 1 away in all directions you see 5 or more walls
                # consolidate this point into a wall, if that doesnt happpen
                # and if looking 2 away in all directions you see less than
                # 7 walls, add a wall, this consolidates and adds walls
                if wallcount_1away >= 5 or wallcount_2away <= 7:
                    new_map[i][j] = WALL
                else:
                    new_map[i][j] = FLOOR
            # this consolidates open space, fills in standalone walls,
            # after generation 5 consolidate walls and increase walking space
            # if there are more than 5 walls nearby make that point a wall,
            # otherwise add a floor
            else:
                # if looking 1 away in all direction you see 5 walls
                # consolidate this point into a wall,
                if wallcount_1away >= 5:
                    new_map[i][j] = WALL
                else:
                    new_map[i][j] = FLOOR

display_cave(new_map)