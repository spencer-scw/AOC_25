from functools import cache
f = open("input.txt", 'r')

devices = {}

for line in f.readlines():
    id, outputs_raw = line.split(':')
    outputs = outputs_raw.split()
    devices[id] = outputs

@cache
def routes_to_out(id):
    if devices[id] == ["out"]:
        return 1
    return sum(routes_to_out(output) for output in devices[id])

print(routes_to_out('you'))
        
