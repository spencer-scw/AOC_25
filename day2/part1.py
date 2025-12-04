from functools import reduce

f = open("input.txt", 'r')
input_lines = f.readlines()

input_lines = [line.strip() for line in input_lines]

range_strings = input_lines[0].split(',')

ranges = []
for range_string in range_strings:
    min, max = range_string.split('-')
    ranges.append((int(min), int(max) + 1))

def check_id(id: str) -> int:
    if len(id) % 2 != 0:
        return 0

    halfway = len(id) // 2
    if id[:halfway] == id[halfway:]:
        return int(id)

    return 0

def range_generator():
    for min, max in ranges:
        for i in range(min, max):
            yield str(i)

total = reduce(lambda acc, range: acc + check_id(range), range_generator(), 0)

print(total)
