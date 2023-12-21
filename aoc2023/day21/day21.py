import aoc

tester = aoc.Tester("Step Counter")


def parse(data: str) -> tuple[tuple[int, int], aoc.Grid2D]:
    grid = {}
    start = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = c
            if c == "S":
                start = (x, y)
    return start, grid


def bfs(start: tuple[int, int], grid: aoc.Grid2D, max_step: int) -> int:
    queue = [(start, 0)]
    _, r, _, _ = aoc.find_extents(grid)
    r += 1

    visited = {}
    while queue:
        pos, step = queue.pop(0)

        if step > max_step:
            break

        if pos in visited:
            continue

        visited[pos] = step

        x, y = pos

        for dx, dy in aoc.DIRECTIONS2D_4:
            new_pos = (x + dx, y + dy)
            if new_pos not in visited:
                mod_pos = (new_pos[0] % r, new_pos[1] % r)
                if mod_pos in grid and grid[mod_pos] != "#":
                    queue.append((new_pos, step + 1))

    # aoc.print_map(visited, func=lambda g, x: f"{g[x]:^5d}", missing="  .  ")
    count = 0
    for steps in visited.values():
        if steps % 2 == max_step % 2:
            count += 1

    return count


def qsdm(grid: aoc.Grid2D, start: tuple[int, int], steps: int) -> int:
    # quadratic sequence difference method
    # needed help from Reddit to even know that this was a way of solving the problem
    _, r, _, _ = aoc.find_extents(grid)
    r += 1  # width of tile

    mod = steps % r
    u_1 = bfs(start, grid, mod)
    u_2 = bfs(start, grid, mod + r)
    u_3 = bfs(start, grid, mod + r * 2)

    diff_1 = u_2 - u_1
    diff_2 = u_3 - u_2
    second_diff = diff_2 - diff_1

    # u_n = an^2 + bn + c
    # 2a = second_diff
    # 3a + b = u_2 - u_1
    # a + b + c = u_1
    a = second_diff // 2
    b = diff_1 - 3 * a
    c = u_1 - a - b

    x = steps // r + 1
    return a * x**2 + b * x + c


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    start, grid = parse(aoc.read_input("input_test"))
    visit = bfs(start, grid, 6)
    t.test_value(visit, 16)

    t.test_value(bfs(start, grid, 10), 50)
    t.test_value(bfs(start, grid, 50), 1594)
    t.test_value(bfs(start, grid, 100), 6536)
    # t.test_value(bfs(start, grid, 500), 167004)

    # my interpretation is that:
    # the input data does not have the same properties as the test data
    # so the quadratic sequence difference method does not work for the test data :(
    # the input data has a direct route to the edge (both directions),
    # while the test data has rocks in the way
    t.test_value(qsdm(grid, start, 10), 50)
    t.test_value(qsdm(grid, start, 50), 1594)
    t.test_value(qsdm(grid, start, 100), 6536)
    t.test_value(qsdm(grid, start, 500), 167004)
    t.test_value(qsdm(grid, start, 1000), 668697)
    t.test_value(qsdm(grid, start, 5000), 16_733_044)


run_tests(tester)

data = aoc.read_input()
start, grid = parse(data)

tester.test_section("Part 1")
solution_1 = qsdm(grid, start, 64)
tester.test_solution(solution_1, 3809)

tester.test_section("Part 2")
solution_2 = qsdm(grid, start, 26_501_365)
tester.test_solution(solution_2, 629_720_570_456_311)
