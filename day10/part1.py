from itertools import combinations_with_replacement
from functools import reduce
from operator import xor
f = open("input.txt", 'r')

class Machine:
    def __init__(self, light_diagram, button_schematic):
        self.light_diagram: int = light_diagram
        self.button_schematic: list(int) = button_schematic
        self.lights = 0

    def _machine_configured(self, button_combo):
        return self.light_diagram == reduce(xor, button_combo)

    def __str__(self):
        return ''.join(['#' if light else '.' for light in self.lights])

    def check_presses(self):
        presses = 1
        while True:
            for button_combo in combinations_with_replacement(self.button_schematic, presses):
                if self._machine_configured(button_combo):
                    return presses
            presses += 1

def convert_button_to_binary(button: tuple[int], length: int):
    binstring = [0] * length
    for val in button:
        binstring[val] =  1

    return eval('0b' + ''.join([str(val) for val in binstring]))

machines = []
for line in f.readlines():
    lights, *buttons, _ = line.split()
    light_diagram = eval("0b" + ''.join([str(int(light == '#')) for light in lights[1:-1]]))
    button_schematic = [convert_button_to_binary(tuple([int(val) for val in button[1:-1].split(',')]), len(lights) - 2) for button in buttons]
    machines.append(Machine(light_diagram, button_schematic))

total = sum([machine.check_presses() for machine in machines])
print(total)



