f = open("input.txt", 'r')
input_lines = f.readlines()

input_lines = [line.strip() for line in input_lines]

def optimal_digit_finder(bank, trimmed_length, digits_required_after, joltage_so_far):
    # base case: digits_required_after is zero
    if digits_required_after == 0:
        return joltage_so_far

    max_digit = max([int(b) for b in bank])
    max_location = bank.find(str(max_digit))

    # base case: digits_required_after is exactly how much room is left 
    if max_location + digits_required_after == len(bank):
        return ''.join([joltage_so_far, bank[max_location:]])

    # recursive greedy case: lower standards until we have plenty of room for the rest of the digits; take the highest and continue

    temp_bank = bank

    while True:
        if max_location + digits_required_after <= len(bank):
            new_bank = bank[max_location + 1:]
            new_joltage_so_far = ''.join([joltage_so_far,  str(max_digit)])
            return optimal_digit_finder(new_bank, trimmed_length + max_location + 1, digits_required_after - 1, new_joltage_so_far)

        temp_bank = temp_bank.replace(str(max_digit), '0')
        max_digit = max([int(b) for b in temp_bank])
        max_location = temp_bank.find(str(max_digit)) 


total_joltage = 0
for bank in input_lines:
    joltage = int(optimal_digit_finder(bank, 0, 12, ''))
    # print(joltage)
    total_joltage += joltage

print(total_joltage)
