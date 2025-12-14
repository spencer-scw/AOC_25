import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

f = open("test.txt", 'r')

def vector_add(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def vector_le(v1, v2):
    return all(x <= y for x, y in zip(v1, v2))

class Machine:
    def __init__(self, joltage_requirement, button_schematic):
        self.joltage_requirement = np.array(joltage_requirement)
        self.button_matrix = np.array(button_schematic).T # num_lights x num_buttons

    def check_presses(self):
        num_buttons = self.button_matrix.shape[1]
        
        # Objective: Minimize sum of presses (1 * x_1 + 1 * x_2 + ...)
        c = np.ones(num_buttons)

        # Constraint: Ax = target
        # We use a LinearConstraint where lb (lower bound) and ub (upper bound) 
        # are both the target, forcing equality.
        constraints = LinearConstraint(self.button_matrix, self.joltage_requirement, self.joltage_requirement)

        # Variable bounds: 0 to infinity, and they must be Integers
        integrality = np.ones(num_buttons) # 1 = Integer, 0 = Continuous
        bounds = Bounds(lb=0, ub=np.inf)

        # Run the Mixed-Integer Linear Programming solver
        res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)

        # Check if a solution was found
        if res.success:
            # The result is floating point (e.g. 5.0000001), round it safely
            presses = np.round(res.x).astype(int)
    
            # Double check the math (floating point errors can rarely happen)
            if np.all(self.button_matrix @ presses == self.joltage_requirement):
                return int(np.sum(presses))

def to_mask(button: tuple[int], length: int):
    mask = [0] * length
    for val in button:
        mask[val] =  1
    return tuple(mask)

machines = []
for line in f.readlines():
    lights, *buttons, joltages = line.split()
    joltage_requirement = tuple([int(j) for j in joltages.strip('{}').split(',')])
    button_schematic = [to_mask(tuple([int(val) for val in button[1:-1].split(',')]), len(lights) - 2) for button in buttons]
    machines.append(Machine(joltage_requirement, button_schematic))

total = sum([machine.check_presses() for machine in machines])
print(total)
