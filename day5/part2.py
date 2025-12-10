f = open("input.txt", 'r')
input_lines = f.readlines()

ranges = []
total = 0

for line in input_lines:
    line = line.strip()
    if line == '':
        break

    # for each range I already have, reduce the current range's bounds if it overlaps.
    # If the range is fully captured, don't even bother appending it.
    curr_lower, curr_upper = [int(val) for val in line.split('-')]

    captured_ranges = []
    for i, (lower, upper) in enumerate(ranges):
        # perforation
        if curr_lower <= lower and curr_upper >= upper:
            captured_ranges.append(i)
            total -= upper - lower + 1
            continue
        
        # trim range
        if curr_upper >= lower and curr_upper < upper:
            curr_upper = lower - 1
        if curr_lower <= upper and curr_lower > lower:
            curr_lower = upper + 1

    [ranges.pop(i) for i in reversed(captured_ranges)]

    difference = curr_upper - curr_lower
    if difference >= 0:
        total += difference + 1
        ranges.append((curr_lower, curr_upper))

print(total)
