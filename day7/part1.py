import re
f = open("test.txt", 'r')
beam_indices = set()
total_splits = 0
for i, line in enumerate(f.readlines()):
    if i == 0:
        beam_indices.add(line.find('S'))
    if i % 2 == 0:
        splitters = set([m.start() for m in re.finditer(r'\^', line)])

        previous_length = len(beam_indices)
        beam_indices.difference_update(splitters)
        total_splits += previous_length - len(beam_indices)

        new_beams = {splitter + 1 for splitter in splitters}.union({splitter - 1 for splitter in splitters})
        beam_indices = beam_indices.union(new_beams)

print(total_splits)
