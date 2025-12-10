import re
f = open("input.txt", 'r')
timeline_indices = {}

class Timeline_Manager:
    def __init__(self):
        self.timeline_indices = {}

    def add(self, index, amount = 1):
        if self.timeline_indices.get(index):
            self.timeline_indices[index] += amount
        else:
            self.timeline_indices[index] = amount

    def remove(self, index):
        self.timeline_indices[index] = 0

    def split(self, index):
        if self.timeline_indices.get(index):
            self.add(index - 1, self.timeline_indices[index])
            self.add(index + 1, self.timeline_indices[index])
            self.remove(index)

    def total(self):
        return sum([timeline for timeline in self.timeline_indices.values()])

    def __str__(self):
        return str(self.timeline_indices)

timelines = Timeline_Manager()
for i, line in enumerate(f.readlines()):
    if i == 0:
        timelines.add(line.find('S'))
    elif i % 2 == 0:
        splitters = [m.start() for m in re.finditer(r'\^', line)]

        [timelines.split(splitter) for splitter in splitters]

print(timelines.total())
