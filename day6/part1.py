f = open("input.txt", 'r')
input_lines = f.readlines()

rows = [line.strip().split() for line in input_lines]

print(
    sum(
        [eval(
              ''.join([f"{operand} {operator} " for operand in operands])[:-2]
          ) for *operands, operator in zip(*rows)]
    )
)
