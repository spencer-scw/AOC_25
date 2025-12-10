from math import prod
import itertools
f = open("input.txt", 'r')
tiles = [tuple([int(coord) for coord in coordinates.split(',')]) for coordinates in f.readlines()]

tiles.append(tiles[0])

unique_x = sorted(list(set(t[0] for t in tiles)))
unique_y = sorted(list(set(t[1] for t in tiles)))

x_map = {val: i for i, val in enumerate(unique_x)}
y_map = {val: i for i, val in enumerate(unique_y)}

x_lookup = {i: val for i, val in enumerate(unique_x)}
y_lookup = {i: val for i, val in enumerate(unique_y)}

tiles = [(x_map[x], y_map[y]) for x, y in tiles]

max_dims = tuple(max(dim) + 2 for dim in zip(*tiles))
min_dims = tuple(min(dim) for dim in zip(*tiles))

def area(p, q):
    real_p = (x_lookup[p[0]], y_lookup[p[1]])
    real_q = (x_lookup[q[0]], y_lookup[q[1]])
    return prod([abs(p_i - q_i) + 1 for p_i, q_i in zip(real_p, real_q)])

def cardinals(tile):
    x, y = tile
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

def get_outer_line_coords(p, q):
    x_limits = sorted([p[1], q[1]])
    y_limits = sorted([p[0], q[0]])
    x_limits[1] += 1
    y_limits[1] += 1

    if p[0] == q[0]:
        coords = [(p[0], q_i) for q_i in range(*x_limits)]
        if p[1] < q[1]:
            return coords
        else:
            return reversed(coords)
    else:
        coords = [(p_i, q[1]) for p_i in range(*y_limits)]
        if p[0] < q[0]:
            return reversed(coords)
        else:
            return coords

clockwise = 1
def get_inner_line_coords(p, q):
    x_limits = sorted([p[1], q[1]])
    y_limits = sorted([p[0], q[0]])
    x_limits[1] += 1
    y_limits[1] += 1

    if p[0] == q[0]:
        direction = 0
        if p[1] < q[1]:
            direction = -1 * clockwise
        else:
            direction = clockwise

        return [(p[0 ] + direction, q_i) for q_i in range(*x_limits)]
    elif p[1] == q[1]:
        direction = 0
        if p[0] < q[0]:
            direction = clockwise
        else:
            direction = -1 * clockwise

        return [(p_i, q[1] + direction) for p_i in range(*y_limits)]


outer_edge_tiles = set()
inner_edge_tiles = set()
for p, q in itertools.pairwise(tiles):
    inner_edge_tiles.update(get_inner_line_coords(p, q))
    outer_edge_tiles.update(get_outer_line_coords(p, q))

inner_edge_tiles.difference_update(outer_edge_tiles)

def get_rectangle_area_if_valid(p, q, max):
    if area(p, q) <= max:
        return 0
        
    p1, p2 = p
    q1, q2 = q
    corners = [(p1, p2), (p1, q2), (q1, q2), (q1, p2), (p1, p2)]
    border_tiles = [p]
    for corner1, corner2 in itertools.pairwise(corners):
        border_tiles.extend(get_outer_line_coords(corner1, corner2))

    inside = False
    for border_tile in border_tiles:
        if border_tile in outer_edge_tiles:
            inside = False
            continue
        else:
            if border_tile in inner_edge_tiles:
                inside = True
                continue
            elif inside:
                continue
            else:
                return 0

    return area(p, q)

max_area = 0
for i, (p, q) in enumerate(itertools.combinations(tiles, 2)):
    max_area = max(max_area, get_rectangle_area_if_valid(p, q, max_area))

print(max_area)

# # diagnostic printing, inefficient on input
# grid = [["." for _ in range(max_dims[0])] for _ in range(max_dims[1])]
# for x, y in outer_edge_tiles:
#     grid[y][x] = '#'
# for x, y in inner_edge_tiles:
#     grid[y][x] = '_'
# [print(''.join(row)) for row in grid]
