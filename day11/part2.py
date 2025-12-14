from functools import cache
f = open("input.txt", 'r')

devices = {}

for line in f.readlines():
    id, outputs_raw = line.split(':')
    outputs = outputs_raw.split()
    devices[id] = outputs

@cache
def routes_to_out(id, dac = False, fft = False):
    if id == "dac":
        dac = True
    if id == "fft":
        fft = True
    if devices[id] == ["out"]:
        if dac and fft:
            return 1
        else:
            return 0
    return sum(routes_to_out(output, dac, fft) for output in devices[id])

print(routes_to_out('svr'))
        
