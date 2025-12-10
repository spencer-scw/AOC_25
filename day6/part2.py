f = open("input.txt", 'r')
input_lines = f.readlines()

rows = [list(reversed(line[:-1])) for line in input_lines]

total = 0
recent_nums = []
for col in zip(*rows):
    *digits, operator = col
    num = ''.join(digits)
    if num.strip() == '':
        continue
    recent_nums.append(num)
    if operator != ' ':
        equation = ''.join([f"{num} {operator} " for num in recent_nums])
        total += eval(equation[:-2])
        recent_nums = []

print(total)
    
    
