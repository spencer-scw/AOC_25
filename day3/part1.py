f = open("input.txt", 'r')
input_lines = f.readlines()

input_lines = [line.strip() for line in input_lines]

total_joltage = 0
for bank in input_lines:
    max_digit = max([int(b) for b in bank])
    max_location = bank.find(str(max_digit)) 

    if max_location >= len(bank) - 1:
        temp_bank = bank.replace(str(max_digit), '0')
        max_digit = max([int(b) for b in temp_bank])
        max_location = temp_bank.find(str(max_digit)) 

    next_digit = max([int(b) for b in bank[max_location + 1:]])
    joltage = int(''.join([str(max_digit), str(next_digit)]))
    total_joltage += joltage

print(total_joltage)
