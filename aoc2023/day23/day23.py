import heapq
import aoc

tester = aoc.Tester("A Long Walk")


def parse(data: str) -> tuple[aoc.Grid2D, tuple[int, int], tuple[int, int]]:
    grid = {}
    start = (0, 0)
    end = (0, 0)
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c != "#":
                grid[(x, y)] = c

            if c == "S":
                start = (x, y)

            if c == "E":
                end = (x, y)

    return grid, start, end


def create_compressed_graph(
    grid: aoc.Grid2D,
    start: tuple[int, int],
    slopes: bool = True,
) -> dict[tuple[int, int], set[tuple[tuple[int, int], int]]]:
    # create a graph with only junctions and the start and end
    queue = [(start, start, 0)]
    visited = set()
    graph = {start: set()}

    while queue:
        pos, source, dist = queue.pop()

        visited.add(pos)

        if grid[pos] == "E":
            # we treat the end as a junction with no return
            graph[pos] = {(source, dist)}
            graph[source].add((pos, dist))
            continue

        if is_junction(grid, pos) or (slopes and grid[pos] in "<>^v"):
            if pos not in graph:
                graph[pos] = set()

            if not slopes:
                # we treat slopes as junctions with no return
                graph[pos].add((source, dist))
            graph[source].add((pos, dist))

            dist = 0
            source = pos

        if slopes and grid[pos] in "<>^v":
            # if we are in slopes mode, we can only go in the direction the slope is pointing
            match grid[pos]:
                case "<":
                    dx, dy = -1, 0
                case ">":
                    dx, dy = 1, 0
                case "^":
                    dx, dy = 0, -1
                case "v":
                    dx, dy = 0, 1
                case _:
                    raise ValueError(f"Invalid direction {grid[pos]}")
            neighbors = [(pos[0] + dx, pos[1] + dy)]
        else:
            # we can go in all directions
            neighbors = [(pos[0] + dx, pos[1] + dy) for dx, dy, in aoc.DIRECTIONS2D_4]

        # add all neighbors to the queue if they are part of a route or not visited
        # we also check if the neighbor is an already visited junction -> add the edge to the graph
        for new_pos in neighbors:
            if new_pos in grid and new_pos not in visited:
                queue.append((new_pos, source, dist + 1))

            elif new_pos in graph and new_pos != source:
                graph[new_pos].add((source, dist + 1))
                graph[source].add((new_pos, dist + 1))
    return graph


def is_junction(
    grid: aoc.Grid2D,
    pos: tuple[int, int],
) -> bool:
    # a junction is a position with more than 2 neighbors
    directions = 0
    for dx, dy in aoc.DIRECTIONS2D_4:
        new_pos = (pos[0] + dx, pos[1] + dy)
        if new_pos in grid:
            directions += 1
    junction = directions > 2
    return junction


def find_longest_path_in_graph(
    graph: dict[tuple[int, int], set[tuple[tuple[int, int], int]]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    queue = [(0, start, {start})]
    next_to_last = list(graph[end])[0]
    exit_path = [path for path in graph[next_to_last[0]] if path[0] == end]

    max_dist = 0
    while queue:
        dist, pos, path = heapq.heappop(queue)

        if pos == end:
            max_dist = min(max_dist, dist)

        if pos == next_to_last[0]:
            # we reached the next to last junction, we do not need to check any
            # other paths than towards the exit (or we will never be able to return...)
            neighbors = exit_path
        else:
            neighbors = graph[pos]

        for next_pos, next_dist in neighbors:
            if next_pos not in path:
                new_path = set(path) | {next_pos}
                heapq.heappush(queue, (dist - next_dist, next_pos, new_path))

    return -max_dist


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    grid, start, end = parse(aoc.read_input("input_test"))

    graph = create_compressed_graph(grid, start, slopes=True)
    t.test_value(find_longest_path_in_graph(graph, start, end), 94)

    graph = create_compressed_graph(grid, start, slopes=False)
    expected_graph = {
        (1, 0): {((3, 5), 15)},
        (3, 5): {((1, 0), 15), ((5, 13), 22), ((11, 3), 22)},
        (5, 13): {((3, 5), 22), ((13, 19), 38), ((13, 13), 12)},
        (11, 3): {((21, 11), 30), ((3, 5), 22), ((13, 13), 24)},
        (13, 13): {((13, 19), 10), ((21, 11), 18), ((5, 13), 12), ((11, 3), 24)},
        (13, 19): {((19, 19), 10), ((13, 13), 10), ((5, 13), 38)},
        (19, 19): {((21, 22), 5), ((21, 11), 10), ((13, 19), 10)},
        (21, 11): {((19, 19), 10), ((11, 3), 30), ((13, 13), 18)},
        (21, 22): {((19, 19), 5)},
    }
    t.test(
        graph == expected_graph,
        message="Graph is incorrect!",
        success_message="Graph is correct",
    )
    t.test_value(find_longest_path_in_graph(graph, start, end), 154)


run_tests(tester)

data = aoc.read_input()
grid, start, end = parse(data)


tester.test_section("Part 1")
graph = create_compressed_graph(grid, start, slopes=True)
solution_1 = find_longest_path_in_graph(graph, start, end)
tester.test_solution(solution_1, 2406)

tester.test_section("Part 2")
graph = create_compressed_graph(grid, start, slopes=False)
solution_2 = find_longest_path_in_graph(graph, start, end)
tester.test_greater_than(solution_2, 6026)
tester.test_greater_than(solution_2, 6158)
tester.test_solution(solution_2, 6630)
