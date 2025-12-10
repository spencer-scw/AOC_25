f = open("input.txt", 'r')
input_lines = f.readlines()

ranges = []
num_fresh_ingredients = 0

for line in input_lines:
    line = line.strip()
    if line.find('-') != -1:
        ranges.append(tuple([int(val) for val in line.split('-')]))
    elif line != '':
        ingredient_id = int(line)
        for lower, upper in ranges:
            if ingredient_id <= upper and ingredient_id >= lower:
                num_fresh_ingredients += 1
                break

print(num_fresh_ingredients)


    
