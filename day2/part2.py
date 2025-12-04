from functools import reduce
from re import finditer

f = open("input.txt", 'r')
input_lines = f.readlines()

input_lines = [line.strip() for line in input_lines]

range_strings = input_lines[0].split(',')

ranges = []
for range_string in range_strings:
    min, max = range_string.split('-')
    ranges.append((int(min), int(max) + 1))

def substringer(id: str):
    for i in range(len(id) // 2 + 1):
        yield id[:i]

def check_id(id: str) -> int:
    substrings = substringer(id)
    for pattern in substrings:
        num_matches = sum(1 for m in finditer(pattern, id))
        if num_matches <= 1:
            return 0
        if len(pattern) * num_matches == len(id):
            return int(id)
    return 0

def range_generator():
    for min, max in ranges:
        for i in range(min, max):
            yield str(i)

total = reduce(lambda acc, range: acc + check_id(range), range_generator(), 0)

print(total)
