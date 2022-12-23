import collections
import typing

import aoc

Tuple2: typing.TypeAlias = tuple[int, int]

NW = (-1, -1)
W = (-1, 0)
SW = (-1, 1)
S = (0, 1)
SE = (1, 1)
E = (1, 0)
NE = (1, -1)
N = (0, -1)

tester = aoc.Tester("Unstable Diffusion")


def parse_input(filename: str) -> set[Tuple2]:
    elves = set()
    data = aoc.read_input(filename)
    y = 0
    for line in data.splitlines():
        x = 0
        for c in line:
            if c == "#":
                elves.add((x, y))
            x += 1
        y += 1

    return elves


def has_neighbors(elves: set[Tuple2], *directions: Tuple2) -> bool:
    for d in directions:
        if d in elves:
            return True
    return False


def spread_elves(elves: set[Tuple2], iteration: int = 0):
    proposals = set()
    collisions = set()
    next_move = {}
    direction_order = collections.deque(["N", "S", "W", "E"])
    direction_order.rotate(-iteration)

    for elf in elves:
        n = aoc.add_tuple(elf, N)
        ne = aoc.add_tuple(elf, NE)
        e = aoc.add_tuple(elf, E)
        se = aoc.add_tuple(elf, SE)
        s = aoc.add_tuple(elf, S)
        sw = aoc.add_tuple(elf, SW)
        w = aoc.add_tuple(elf, W)
        nw = aoc.add_tuple(elf, NW)

        direction = None
        if has_neighbors(elves, n, ne, e, se, s, sw, w, nw):
            for d in direction_order:
                match d:
                    case "N":
                        if not has_neighbors(elves, n, ne, nw):
                            direction = n
                            break
                    case "S":
                        if not has_neighbors(elves, s, se, sw):
                            direction = s
                            break
                    case "W":
                        if not has_neighbors(elves, w, nw, sw):
                            direction = w
                            break
                    case "E":
                        if not has_neighbors(elves, e, ne, se):
                            direction = e
                            break

        if direction:
            next_move[elf] = direction
            if direction not in proposals:
                proposals.add(direction)
            else:
                collisions.add(direction)
        else:
            next_move[elf] = elf

    new_elves = set()
    moved = 0
    for elf, pos in next_move.items():
        if elf != pos:
            moved += 1

        if pos not in collisions:
            new_elves.add(pos)
        else:
            new_elves.add(elf)
    # aoc.print_set(new_elves, border=1)
    # print(f"{iteration=} {moved=}")
    assert len(elves) == len(new_elves)
    return new_elves, moved


def relax_elves(elves: set[Tuple2], max_iterations: int = 0) -> tuple[set[Tuple2], int]:
    elves, n = spread_elves(elves)
    iterations = 1
    while n > 0:
        elves, n = spread_elves(elves, iterations)
        iterations += 1
        if 0 < max_iterations <= iterations:
            break

    return elves, iterations


def count_empty_space(elves: set[Tuple2]) -> int:
    elves, _ = relax_elves(elves, max_iterations=10)
    minx, maxx, miny, maxy = aoc.find_extents(elves)
    # aoc.print_set(elves)
    area = (maxx - minx + 1) * (maxy - miny + 1)
    return area - len(elves)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    elves = parse_input("test_input_s")
    t.test_value(count_empty_space(elves), 25)

    elves = parse_input("test_input_m")
    t.test_value(count_empty_space(elves), 110)

    relaxed_elves, iterations = relax_elves(elves)
    t.test_value(iterations, 20)


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(count_empty_space(parse_input("input")), 4247)

tester.test_section("Part 2")
_, rounds = relax_elves(parse_input("input"))
tester.test_solution(rounds, 1049)
