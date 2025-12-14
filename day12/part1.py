from math import prod
from partition import solve_recursively
from piece import Piece
f = open("my.txt", 'r')

pieces = []
grids = []
curr_piece = []
curr_uid = ''

ratios = []

# read input
for line in f.readlines():
    if line.strip() == '':
        pieces.append(Piece(curr_uid, curr_piece))
        curr_piece = []
    elif len(pieces) < 6:
        if line.find(':') != -1:
            curr_uid = line[0]
        else:
            curr_piece.append(line.strip())

    else:
        dimensions_raw, counts_raw = line.split(':')
        dimensions = [int(dim) for dim in dimensions_raw.split('x')]
        counts = [int(count) for count in counts_raw.split()]
        grids.append({"dimensions": dimensions, "counts": counts})

        ratio = sum(counts) * 7 / prod(dimensions)
        ratios.append(ratio)

##
total = 0
for grid in grids:
    if solve_recursively(*grid.get('dimensions'), pieces, grid.get('counts')):
        total += 1

print(f"Final total: {total}")
