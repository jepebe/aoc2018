import heapq

import aoc

W = (-1, 0)
S = (0, 1)
E = (1, 0)
N = (0, -1)

tester = aoc.Tester("Blizzard Basin")


def parse_input(filename: str):
    data = aoc.read_input(filename)

    # grid = {}
    blizzards = {}

    max_x = 0
    max_y = 0
    blizzard_index = 0
    for y, line in enumerate(data.splitlines()):
        if y > max_y:
            max_y = y
        for x, c in enumerate(line):
            if x > max_x:
                max_x = x

            match c:
                case ">" | "v" | "<" | "^":
                    blizzards[(x, y)] = [(x, y, c, blizzard_index, 0)]
                    blizzard_index += 1

    print_blizzards(max_x, max_y, blizzards)

    return max_x, max_y, blizzards


def print_blizzards(max_x, max_y, blizzards):
    blizzards = dict(blizzards)
    blizzards[0, 0] = []
    blizzards[max_x, max_y] = []

    def fn(items, pos):
        if pos == (1, 0):
            return "S"
        if pos == (max_x - 1, max_y):
            return "E"

        if pos[0] == 0 or pos[0] == max_x or pos[1] == 0 or pos[1] == max_y:
            return "#"

        if pos not in items:
            return "."

        if len(items[pos]) == 1:
            return items[pos][0][2]
        else:
            return str(len(items[pos]))

    # aoc.print_map(blizzards, func=fn, missing_func=fn)


def simulate_blizzards(max_x, max_y, blizzards):
    new_blizzards = {}
    for pos, blizzard_collection in blizzards.items():
        for x, y, c, i, t in blizzard_collection:
            match c:
                case ">":
                    (nx, ny) = aoc.add_tuple((x, y), E)
                case "v":
                    (nx, ny) = aoc.add_tuple((x, y), S)
                case "<":
                    (nx, ny) = aoc.add_tuple((x, y), W)
                case "^":
                    (nx, ny) = aoc.add_tuple((x, y), N)
                case _:
                    assert False, f"Unknown blizzard type {c} {i} {(x, y)}"

            if nx == 0:
                nx = max_x - 1
            if nx == max_x:
                nx = 1
            if ny == 0:
                ny = max_y - 1
            if ny == max_y:
                ny = 1

            if (nx, ny) not in new_blizzards:
                new_blizzards[(nx, ny)] = []

            new_blizzards[(nx, ny)].append((nx, ny, c, i, t))
    # print_blizzards(max_x, max_y, new_blizzards)
    return new_blizzards


def find_neighbors(max_x, max_y, p, blizzards, end):
    neighbors = []
    for d in (N, E, S, W):
        (x, y) = aoc.add_tuple(p, d)
        if (x, y) == end:
            neighbors.append((x, y))
        if 0 < x < max_x and 0 < y < max_y:
            if (x, y) not in blizzards:
                neighbors.append((x, y))

    if p not in blizzards:
        neighbors.append(p)  # wait one minute
    return neighbors


def find_path(max_x, max_y, blizzards, start: tuple[int, int], end: tuple[int, int]):
    blizzards_in_time = {
        0: blizzards,
        1: simulate_blizzards(max_x, max_y, blizzards)
    }

    dist = {(0, start[0], start[1]): 0}
    queue = [(0, start[0], start[1])]

    while queue:
        (t, x, y) = heapq.heappop(queue)

        if (x, y) == end:
            return t, blizzards_in_time[t]

        if t + 1 not in blizzards_in_time:
            blizzards_in_time[t + 1] = simulate_blizzards(max_x, max_y, blizzards_in_time[t])

        neighbors = find_neighbors(max_x, max_y, (x, y), blizzards_in_time[t + 1], end)

        for nx, ny in neighbors:
            nd = t + 1
            if (t + 1, nx, ny) not in dist or nd < dist[(t + 1, nx, ny)]:
                dist[(t + 1, nx, ny)] = nd
                heapq.heappush(queue, (t + 1, nx, ny))


def find_snack_path(max_x, max_y, blizzards):
    t1, blizzards = find_path(max_x, max_y, blizzards, (1, 0), (max_x - 1, max_y))
    t2, blizzards = find_path(max_x, max_y, blizzards, (max_x - 1, max_y), (1, 0))
    t3, blizzards = find_path(max_x, max_y, blizzards, (1, 0), (max_x - 1, max_y))
    return t1 + t2 + t3


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    max_x, max_y, blizzards = parse_input("test_input")
    dist, _ = find_path(max_x, max_y, blizzards, start=(1, 0), end=(max_x - 1, max_y))
    t.test_value(dist, 18)
    dist = find_snack_path(max_x, max_y, blizzards)
    t.test_value(dist, 54)


run_tests(tester)

max_x, max_y, blizzards = parse_input("input")

tester.test_section("Part 1")
tester.test_solution(find_path(max_x, max_y, blizzards, (0, 1), (max_x - 1, max_y))[0], 257)

tester.test_section("Part 2")
tester.test_solution(find_snack_path(max_x, max_y, blizzards), 828)
