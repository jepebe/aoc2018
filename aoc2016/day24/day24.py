import itertools
import typing

import aoc

tester = aoc.Tester("Air Duct Spelunking")

Vec2: typing.TypeAlias = tuple[int, int]


def parse_grid(data: str) -> tuple[dict[Vec2, str], dict[str, Vec2]]:
    grid = {}
    checkpoints = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c in "0123456789":
                checkpoints[c] = (x, y)
                c = "."
            grid[(x, y)] = c
    return grid, checkpoints


def bfs(grid: dict, start_position: Vec2):
    distance_map = {}
    queue = []
    distance_map[start_position] = 0
    queue.append(start_position)

    while len(queue) > 0:
        v = queue.pop(0)

        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            w = aoc.add_tuple(v, direction)
            if w in grid and grid[w] == ".":
                if w not in distance_map:
                    distance_map[w] = distance_map[v] + 1
                    queue.append(w)

    return distance_map


def find_shortest_path(filename: str, finish_at_start: bool = False) -> int:
    grid, checkpoints = parse_grid(aoc.read_input(filename))
    distances = {}
    for i, p in checkpoints.items():
        dmap = bfs(grid, checkpoints[i])
        for t, tp in checkpoints.items():
            if i != t:
                distances[(i, t)] = dmap[tp]

    nodes = [p for p in checkpoints.keys() if p != "0"]
    shortest_path = 999999999
    for permutation in itertools.permutations(nodes):
        permutation = "0", *permutation
        if finish_at_start:
            permutation = *permutation, "0"

        length = 0
        for i in range(len(permutation) - 1):
            f = permutation[i]
            t = permutation[i + 1]
            length += distances[(f, t)]
        if length < shortest_path:
            shortest_path = length

    return shortest_path


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    t.test_value(find_shortest_path("test_input"), 14)


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(find_shortest_path("input"), 474)

tester.test_section("Part 2")
tester.test_solution(find_shortest_path("input", finish_at_start=True), 696)
