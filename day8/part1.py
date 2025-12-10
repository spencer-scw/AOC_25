from math import sqrt, prod
from copy import deepcopy
from uniquepq import TopKPruningQueue
f = open("input.txt", 'r')

class Balltree_Node:
    def __init__(self, pivot: tuple(), radius: int = 0, child1 = None, child2 = None):
        self.pivot = pivot
        self.radius = radius
        self.child1: Balltree_Node = child1
        self.child2: Balltree_Node = child2

    def __str__(self):
        return self.str_recurisive(0)

    def str_recurisive(self, tab_level):
        out = f"{'\t' * tab_level}pivot: {self.pivot}, radius: {self.radius}"
        if self.child1 is None and self.child2 is None:
            return out
        return f"{out}\n{self.child1.str_recurisive(tab_level + 1)}\n{self.child2.str_recurisive(tab_level + 1)}"

def imax(values: list()):
    m = max(values)
    return values.index(m)

def distance(p, q):
    return sqrt(sum([(p_i - q_i)**2 for p_i, q_i in zip(p, q)]))

def construct_balltree(points: list(tuple())):
    if len(points) == 1:
        return Balltree_Node(points[0])
    else:
        # calculate dimension with greatest spread
        dimension_greatest_spread = imax([max(dimension) - min(dimension) for dimension in zip(*points)])

        # get the median point on that dimension
        sorted_points = sorted(points, key = lambda point: point[dimension_greatest_spread])
        pivot_index = len(sorted_points) // 2
        pivot = sorted_points[pivot_index]

        # partition the points greater and less than the median on that dimension
        left_points = sorted_points[:pivot_index]
        right_points = sorted_points[pivot_index:]

        # Recurse on each partition to calculate children
        left_child = construct_balltree(left_points)
        right_child = construct_balltree(right_points)

        # Use the distance to the pivot of each of the children as the radius
        radius = max(distance(pivot, left_child.pivot) + left_child.radius, distance(pivot, right_child.pivot) + right_child.radius)

        # Construct node with info and return it
        return Balltree_Node(pivot, radius, left_child, right_child)

input_points = [tuple([int(val) for val in line.split(',')]) for line in f.readlines()]

balltree = construct_balltree(input_points)

def get_nearest_neighbor(target: tuple(), pq: TopKPruningQueue, ball_node: Balltree_Node):
    if distance(target, ball_node.pivot) - ball_node.radius >= pq.threshold:
        return pq
    elif ball_node.radius == 0:
        new_dist = distance(target, ball_node.pivot) 
        pq.push(new_dist, (target, ball_node.pivot))
    else:
        child1_distance = distance(target, ball_node.child1.pivot)
        child2_distance = distance(target, ball_node.child2.pivot)

        if child1_distance < child2_distance:
            pq = get_nearest_neighbor(target, pq, ball_node.child1)
            pq = get_nearest_neighbor(target, pq, ball_node.child2)
        else:
            pq = get_nearest_neighbor(target, pq, ball_node.child2)
            pq = get_nearest_neighbor(target, pq, ball_node.child1)
            
    return pq

pq = TopKPruningQueue(1000)
for point in input_points:
    pq = get_nearest_neighbor(point, pq, balltree)

# min_dists = list(pq.get_items())

# [print(min_dist) for min_dist in min_dists]

circuits = [set([point]) for point in input_points]
for _, (point1, point2) in pq.get_items():
    new_circuit = set((point1, point2))
    new_circuits: list(set()) = []
    for circuit in circuits:
        if new_circuit.isdisjoint(circuit):
            new_circuits.append(circuit)
        else:
            new_circuit = new_circuit.union(circuit)
    new_circuits.append(new_circuit)
    circuits = deepcopy(new_circuits)


top3 = sorted([len(circuit) for circuit in circuits])[-3:]
print(prod(top3))
