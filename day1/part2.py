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

    num_string = instruction[1:]
    num_string = ''.join(['00', num_string])

    full_rotations = int(num_string[:-2])
    total_zeros += full_rotations

    amount = int(num_string[-2:])
    started_on_zero = dial_position == 0
    dial_position = (dial_position + direction * amount)

    if not started_on_zero and (dial_position <= 0 or dial_position >= 100):
        total_zeros += 1

    dial_position %= 100

print(total_zeros)
