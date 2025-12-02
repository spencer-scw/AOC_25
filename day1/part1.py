f = open("input.txt", 'r')
input_lines = f.readlines()

input_lines = [line.strip() for line in input_lines]

total_zeros = 0
dial_position = 50

for instruction in input_lines:
    direction_letter = instruction[0]
    direction = 0
    if direction_letter == 'R':
        direction = 1
    if direction_letter == 'L':
        direction = -1

    amount = int(instruction[1:])

    dial_position = (dial_position + direction * amount) % 100

    if dial_position == 0:
        total_zeros += 1

print(total_zeros)
