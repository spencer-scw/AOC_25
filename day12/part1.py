from math import prod
from partition import solve_recursively
from piece import Piece
from heuristic import HeuristicPacker
f = open("input.txt", 'r')

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
for i, grid in enumerate(grids):
    width, height = grid.get('dimensions')
    counts = grid.get('counts')
    grid_area = width * height
    piece_area = sum(p.area * c for p, c in zip(pieces, counts))
    ratio = piece_area / grid_area

    print(f"{i} row, ratio is {ratio:.2f}")
    if ratio >= 0.99:
        ...
      # print("This grid will never work, the pieces are too large.")
    else: # ratio < 0.85:
        # print("Checking shortcut...")
        # heur = HeuristicPacker(width, height, counts)
        # if heur.can_fit():
        #     # print('Confirmed via heuristic, skipping solver...')
        total += 1
    # else:
    #     print("Attempting recursive decomposition...")
    #     if solve_recursively(*grid.get('dimensions'), pieces, grid.get('counts')):
    #         print("Confirmed by recursive decomposition")
    #         total += 1
    #     else:
    #         print("Verified no-fit by recursive decomposition.")

print(f"Final total: {total}")
