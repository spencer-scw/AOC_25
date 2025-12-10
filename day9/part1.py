from math import prod
from itertools import combinations
f = open("input.txt", 'r')
tiles = [tuple([int(coord) for coord in coordinates.split(',')]) for coordinates in f.readlines()]

def area(p, q):
    return prod([abs(p_i - q_i) + 1 for p_i, q_i in zip(p, q)])

max_area = 0
num_combinations = 0
for p, q in combinations(tiles, 2):
    num_combinations += 1
    max_area = max(max_area, area(p, q))

print(num_combinations)
print(max_area)
