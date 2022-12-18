import aoc
from aoc import Tuple3, cube_extents  # Using Tuple3 added 10 ms running time :(

DIRECTIONS_3D = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

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


def parse_input(data: str) -> set[Tuple3]:
    cubes = set()
    for line in data.splitlines():
        x, y, z = tuple(map(int, line.split(sep=",")))
        cubes.add(Tuple3(x, y, z))
    return cubes


def count_exposed_sides(cubes: set[Tuple3], exclude: set[Tuple3] = None) -> tuple[int, set[Tuple3]]:
    if exclude is None:
        exclude = set()

    exposed_neighbors = set()
    exposed_count = 0
    for cube in cubes:
        for d in DIRECTIONS_3D:
            neighbor = cube + d
            if neighbor not in cubes and neighbor not in exclude:
                exposed_neighbors.add(neighbor)
                exposed_count += 1
    return exposed_count, exposed_neighbors


def find_pockets(cubes: set[Tuple3]) -> set[Tuple3]:
    cube_min, cube_max = cube_extents(cubes)

    # add open space around everything
    cube_min -= (1, 1, 1)
    cube_max += (1, 1, 1)

    start = cube_min
    distance_map = {start: 0}
    queue = [start]

    # BFS empty space on the outside
    while len(queue) > 0:
        v = queue.pop(0)

        for direction in DIRECTIONS_3D:
            w = v + direction
            if cube_min <= w <= cube_max:
                if w not in cubes and w not in distance_map:
                    distance_map[w] = distance_map[v] + 1
                    queue.append(w)

    # find cubes that was not touched by the BFS
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
