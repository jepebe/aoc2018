import itertools
import typing

import aoc

Vec2: typing.TypeAlias = tuple[int, int]

tester = aoc.Tester("Grid Computing")


def create_grid():
    data = aoc.read_input()
    grid = {}
    for line in data.splitlines():
        if line.startswith("/"):
            match line.split():
                case [node, size, used, avail, _]:
                    _, x, y = node.split(sep="-")
                    x = int(x[1:])
                    y = int(y[1:])
                    assert size[-1] == "T"
                    assert used[-1] == "T"
                    assert avail[-1] == "T"
                    size = int(size[:-1])
                    used = int(used[:-1])
                    avail = int(avail[:-1])
                    grid[(x, y)] = (size, used, avail)
                case rest:
                    assert False, f"Unhandled node {rest}"

    # print_grid(grid)
    return grid


def print_grid(grid):
    def fn(g, p):
        size, used, avail = g[p]

        if p == (0, 0):
            return "E"

        if used == 0:
            return "_"

        # if used / size < 0.65:
        #     return "."
        #
        # if used / size < 0.75:
        #     return "*"

        if used / size < 0.95:
            return "."

        return "#"

    aoc.print_map(grid, func=fn)


def find_start(grid: dict):
    max_x = max(x[0] for x in grid.keys() if x[1] == 0)
    return max_x, 0


def find_empty(grid: dict):
    for pos, value in grid.items():
        if value[1] == 0:
            return pos
    assert False, "Did not find an empty node!"


def find_viable_pairs(grid: dict[Vec2, tuple[int, int, int]]) -> int:
    viable = []
    for n1, n2 in itertools.permutations(grid.keys(), 2):
        n1_size, n1_used, n1_avail = grid[n1]
        n2_size, n2_used, n2_avail = grid[n2]
        if 0 < n1_used <= n2_avail:
            viable.append(n1)
    return len(viable)


def bfs(grid: dict, start_position: Vec2, target: Vec2, avoid: Vec2):
    distance_map = {}
    queue = []
    distance_map[start_position] = 0
    queue.append(start_position)
    max_avail = grid[start_position][0]

    while len(queue) > 0:
        v = queue.pop(0)

        if v == avoid:
            continue

        if v == target:
            return distance_map[v]

        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            w = aoc.add_tuple(v, direction)
            if w in grid:
                w_size, w_used, w_avail = grid[w]

                if w not in distance_map and w_used <= max_avail:
                    distance_map[w] = distance_map[v] + 1
                    queue.append(w)

    assert False, "Target node not found"


def move_data(grid: dict):
    # move empty to front of payload
    # move payload
    # repeat until (0, 0)
    host = (0, 0)
    payload = find_start(grid)
    empty = find_empty(grid)
    total_moves = 0
    while payload != host:
        target = aoc.add_tuple(payload, (-1, 0))
        moves = bfs(grid, empty, target, payload)
        empty = payload
        payload = target
        total_moves += moves + 1
    return total_moves


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    grid = create_grid()
    find_viable_pairs(grid)
    move_data(grid)


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(find_viable_pairs(create_grid()), 987)

tester.test_section("Part 2")
tester.test_solution(move_data(create_grid()), 220)
