from collections import deque
from itertools import chain

f = open("input.txt", 'r')
input_lines = f.readlines()

input_lines = [list(line.strip()) for line in input_lines]

def row_sliding_window():
    iterator = iter(input_lines)
    window = deque((next(iterator, None) for _ in range(2)), maxlen = 3)
    yield window
    for row in iterator:
        window.append(row)
        yield window
    window.popleft()
    yield window

def sliding_window():
    for row, row_window in enumerate(row_sliding_window()):

        iterator = iter(zip(*row_window))

        window = deque((next(iterator, None) for _ in range(2)), maxlen = 3)
        yield window, (row, 0)
        for col, e in enumerate(iterator):
            window.append(e)
            yield window, (row, col + 1)
        window.popleft()
        yield window, (row, col + 2)

windows = sliding_window()
total_rolls = 0

for window, (row, col) in windows:
    if input_lines[row][col] == '@':
        if sum([val == '@' for val in chain(*tuple(window))]) < 5:
            total_rolls += 1

print(total_rolls)
