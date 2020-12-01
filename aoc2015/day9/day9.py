from dataclasses import dataclass, field
from typing import List, Tuple, Dict

import intcode as ic


@dataclass
class Map:
    nodes: set = field(default_factory=set)
    distances: Dict[Tuple[str, str], int] = field(default_factory=dict)

    def add(self, src, dst, distance):
        self.nodes.add(src)
        self.nodes.add(dst)
        self.distances[(src, dst)] = distance
        self.distances[(dst, src)] = distance

    def first_node(self):
        return list(self.nodes)[0]


def create_map(lines: List[str]):
    routes = Map()
    for line in lines:
        names, distance = line.split("=")
        src, dst = names.strip().split(" to ")
        routes.add(src, dst, int(distance))
    return routes


def visit(routes: Map, visited, distance, paths):
    unvisited_neighbors = [n for n in routes.nodes if n not in visited]

    if len(unvisited_neighbors) == 0:
        paths[' -> '.join(visited)] = distance
    else:
        for n in unvisited_neighbors:
            dist = routes.distances[(visited[-1], n)]
            visit(routes, visited + [n], distance + dist, paths)


def find_shortest(routes):
    paths = {}
    for n in routes.nodes:
        visit(routes, [n], 0, paths)

    min_path = min(paths, key=paths.get)
    max_path = max(paths, key=paths.get)
    print(min_path)
    print(max_path)
    return paths[min_path], paths[max_path]


tester = ic.Tester("All in a single night")

test_map = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

routes = create_map(test_map.splitlines())
shortest = find_shortest(routes)
tester.test_value(shortest, (605, 982))

with open("input") as f:
    lines = f.readlines()

routes = create_map(lines)
shortest = find_shortest(routes)
tester.test_value(shortest, (251, 898), 'solution to exercise 1 = %s and 2 = %s')


