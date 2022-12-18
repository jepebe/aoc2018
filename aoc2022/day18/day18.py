import typing

import aoc

tester = aoc.Tester("Boiling Boulders")

test_data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

Tuple3: typing.TypeAlias = tuple[int, int, int]


def parse_input(data: str) -> set[Tuple3]:
    cubes = set()
    for line in data.splitlines():
        x, y, z = tuple(map(int, line.split(sep=",")))
        cubes.add((x, y, z))
    return cubes


def count_exposed_sides(cubes: set[Tuple3], pockets: set[Tuple3] = None) -> tuple[int, set[Tuple3]]:
    if pockets is None:
        pockets = set()

    exposed_neighbors = set()
    exposed_count = 0
    for cube in cubes:
        for d in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
            neighbor = aoc.add_tuple3(cube, d)
            if neighbor not in cubes and neighbor not in pockets:
                exposed_neighbors.add(neighbor)
                exposed_count += 1
    return exposed_count, exposed_neighbors


def find_pockets(cubes: set[Tuple3]) -> set[Tuple3]:
    min_x = min(c[0] for c in cubes) - 1
    max_x = max(c[0] for c in cubes) + 1
    min_y = min(c[1] for c in cubes) - 1
    max_y = max(c[1] for c in cubes) + 1
    min_z = min(c[2] for c in cubes) - 1
    max_z = max(c[2] for c in cubes) + 1
    start = (min_x, min_y, min_z)

    distance_map = {start: 0}
    queue = [start]

    while len(queue) > 0:
        v = queue.pop(0)

        for direction in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
            w = aoc.add_tuple3(v, direction)
            if min_x <= w[0] <= max_x and min_y <= w[1] <= max_y and min_z <= w[2] <= max_z:
                if w not in cubes and w not in distance_map:
                    distance_map[w] = distance_map[v] + 1
                    queue.append(w)

    _, exposed_neighbors = count_exposed_sides(cubes)
    pocket_cubes = set()
    for cube in exposed_neighbors:
        if cube not in distance_map:
            pocket_cubes.add(cube)

    return pocket_cubes


def count_exposed_sides_not_in_pocket(cubes: set[Tuple3]) -> int:
    pocket_cubes = find_pockets(cubes)
    exposed_count, _ = count_exposed_sides(cubes, pocket_cubes)
    return exposed_count


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    cubes = parse_input(test_data)
    t.test_value(count_exposed_sides(cubes)[0], 64)
    t.test_value(count_exposed_sides_not_in_pocket(cubes), 58)


run_tests(tester)

input_cubes = parse_input(aoc.read_input())

tester.test_section("Part 1")
tester.test_value(count_exposed_sides(input_cubes)[0], 4192, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(count_exposed_sides_not_in_pocket(input_cubes), 2520, "solution to part 2=%s")
