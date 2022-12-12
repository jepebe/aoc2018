import typing

import aoc
import aoc.heightmap

Vec2: typing.TypeAlias = tuple[int, int]

test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def parse_heightmap(data: str):
    elevation_map = {}
    start_pos = None
    end_pos = None
    y = 0
    for line in data.splitlines():
        x = 0
        for c in line:
            match c:
                case "S":
                    start_pos = (x, y)
                    elevation_map[(x, y)] = "a"
                case "E":
                    end_pos = (x, y)
                    elevation_map[(x, y)] = "z"
                case _:
                    elevation_map[(x, y)] = c
            x += 1
        y += 1

    # aoc.heightmap.print_heightmap(elevation_map)
    return elevation_map, start_pos, end_pos


def bfs(elevation_map: dict[Vec2, str], start_positions: list[Vec2]):
    distance_map = {}
    queue = []
    for pos in start_positions:
        distance_map[pos] = 0
        queue.append(pos)

    while len(queue) > 0:
        v = queue.pop(0)
        v_height = elevation_map[v]

        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            w = aoc.add_tuple(v, direction)
            if w in elevation_map:
                w_height = elevation_map[w]
                if w not in distance_map and -1 <= ord(v_height) - ord(w_height) <= 26:
                    distance_map[w] = distance_map[v] + 1
                    queue.append(w)

    return distance_map


tester = aoc.Tester("Hill Climbing Algorithm")

tester.test_section("Tests")

test_grid, test_start, test_end = parse_heightmap(test_data)
test_distance = bfs(test_grid, [test_start])

tester.test_value(test_distance[test_end], 31)

test_start = [pos for pos, elevation in test_grid.items() if elevation == "a"]
test_distance = bfs(test_grid, test_start)
tester.test_value(test_distance[test_end], 29)

tester.test_section("Part 1")
grid, start, end = parse_heightmap(aoc.read_input())
distance = bfs(grid, [start])
tester.test_value(distance[end], 528, "solution to part 1=%s")

tester.test_section("Part 2")
start = [pos for pos, elevation in grid.items() if elevation == "a"]
distance = bfs(grid, start)
tester.test_value(distance[end], 522, "solution to part 2=%s")
