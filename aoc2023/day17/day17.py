import heapq

import aoc

tester = aoc.Tester("Clumsy Crucible")


def parse(data: str):
    grid: aoc.Grid2D = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = int(c)

    return grid


def bfs(grid: aoc.Grid2D, min_distance: int = 1, max_distance: int = 3) -> int:
    start = (0, 0)
    end = max(grid.keys())

    queue = [(0, start, (0, 0))]
    visited = {}

    while queue:
        heat_loss, pos, dxdy = heapq.heappop(queue)

        if pos == end:
            return heat_loss

        if (pos, dxdy) in visited:
            # We already found a better path
            continue

        visited[pos, dxdy] = heat_loss

        for dx, dy in aoc.DIRECTIONS2D_4:
            if (dx, dy) == dxdy or (-dx, -dy) == dxdy:
                continue

            next_heat_loss = heat_loss
            for i in range(1, max_distance + 1):
                nx, ny = pos[0] + dx * i, pos[1] + dy * i

                if (nx, ny) not in grid:
                    break

                next_heat_loss += grid[nx, ny]
                if i >= min_distance:
                    heapq.heappush(queue, (next_heat_loss, (nx, ny), (dx, dy)))

    assert False, "No path found"


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    grid = parse(data)
    t.test_value(bfs(grid), 102)

    t.test_value(bfs(grid, 4, 10), 94)

    data = aoc.read_input("input_test_2")
    grid = parse(data)
    t.test_value(bfs(grid, 4, 10), 71)


run_tests(tester)

data = aoc.read_input()
grid = parse(data)

tester.test_section("Part 1")
solution_1 = bfs(grid)
tester.test_less_than(solution_1, 1151)
tester.test_less_than(solution_1, 968)
tester.test_solution(solution_1, 953)

tester.test_section("Part 2")
solution_2 = bfs(grid, 4, 10)
tester.test_solution(solution_2, 1180)
