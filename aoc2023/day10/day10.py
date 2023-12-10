import aoc

tester = aoc.Tester("Pipe Maze")


def parse(data: str) -> tuple[tuple[int, int], aoc.Grid2D]:
    grid: aoc.Grid2D = {}
    start: tuple[int, int] = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            pos = (x, y)
            if c == "S":
                start = pos
            grid[pos] = c

    return start, grid


def bfs(start: tuple[int, int], grid: aoc.Grid2D) -> dict[tuple[int, int], int]:
    # find all reachable positions and their distance from start
    queue = [(start, 0)]
    visited = {}
    while queue:
        pos, dist = queue.pop(0)
        if pos in visited:
            if visited[pos] > dist:
                visited[pos] = dist
            continue
        visited[pos] = dist

        north = (pos[0], pos[1] - 1)
        south = (pos[0], pos[1] + 1)
        east = (pos[0] + 1, pos[1])
        west = (pos[0] - 1, pos[1])
        match grid[pos]:
            case "|":  # north/south
                if north not in visited and north in grid:
                    queue.append((north, dist + 1))
                if south not in visited and south in grid:
                    queue.append((south, dist + 1))

            case "-":  # east/west
                if east not in visited and east in grid:
                    queue.append((east, dist + 1))
                if west not in visited and west in grid:
                    queue.append((west, dist + 1))

            case "F":  # south/east
                if east not in visited and east in grid:
                    queue.append((east, dist + 1))
                if south not in visited and south in grid:
                    queue.append((south, dist + 1))

            case "7":  # south/west
                if south not in visited and south in grid:
                    queue.append((south, dist + 1))
                if west not in visited and west in grid:
                    queue.append((west, dist + 1))

            case "L":  # north/east
                if north not in visited and north in grid:
                    queue.append((north, dist + 1))
                if east not in visited and east in grid:
                    queue.append((east, dist + 1))

            case "J":  # north/west
                if north not in visited and north in grid:
                    queue.append((north, dist + 1))
                if west not in visited and west in grid:
                    queue.append((west, dist + 1))

            case "S":  # start
                if north not in visited and north in grid and grid[north] in "|F7":
                    queue.append((north, dist + 1))
                if south not in visited and south in grid and grid[south] in "|JL":
                    queue.append((south, dist + 1))
                if east not in visited and east in grid and grid[east] in "-J7":
                    queue.append((east, dist + 1))
                if west not in visited and west in grid and grid[west] in "-FL":
                    queue.append((west, dist + 1))

            case ".":  # ground
                raise ValueError(f"How? {grid[pos]} at {pos}")
            case _:
                raise ValueError(f"Invalid character {grid[pos]} at {pos}")
    return visited


def expand_grid(start: tuple[int, int], grid: aoc.Grid2D) -> aoc.Grid2D:
    # double grid size by extending connection lines
    # we also remove all pipe segments that are not part of the maze
    visited = bfs(start, grid)

    new_grid = {}
    for x, y, pipe in aoc.iterate_grid(grid):
        if (x, y) in visited:
            new_grid[(x * 2, y * 2)] = pipe
        if (x + 1, y) in visited:
            if pipe in "-FLS" and grid[(x + 1, y)] in "-7JS":
                new_grid[(x * 2 + 1, y * 2)] = "-"
        if (x, y + 1) in visited:
            if pipe in "|F7S" and grid[(x, y + 1)] in "|JLS":
                new_grid[(x * 2, y * 2 + 1)] = "|"
        if (x + 1, y + 1) in visited:
            pass
    return new_grid


def find_enclosed(start: tuple[int, int], grid: aoc.Grid2D) -> int:
    # double size of grid to simplify finding enclosed area
    expanded_grid = expand_grid(start, grid)
    # find all grid points that are not pipes
    candidates = set()
    for x, y, pipe in aoc.iterate_grid(expanded_grid):
        if pipe is None:
            candidates.add((x, y))

    # find all connected grid points that are not pipes using BFS
    visited = {}
    marker = 0
    dirty_markers = set()
    for candidate in candidates:
        if candidate not in visited:
            queue = [candidate]
            while queue:
                x, y = queue.pop(0)
                if (x, y) in visited:
                    continue
                visited[(x, y)] = marker

                for dx, dy in aoc.DIRECTIONS2D_4:
                    next_pos = (x + dx, y + dy)
                    # only expand into possible candidates
                    if next_pos in candidates:
                        queue.append(next_pos)
                    # if we leave the grid we are not enclosed
                    if next_pos not in candidates and next_pos not in expanded_grid:
                        dirty_markers.add(marker)

            marker += 1

    # exclude all grid points that are dirty
    enclosed_grid = {}
    for x, y, pipe in aoc.iterate_grid(expanded_grid):

        if x % 2 == 1 or y % 2 == 1:
            continue

        if (x, y) in visited:
            marker = visited[(x, y)]
            if marker not in dirty_markers:
                enclosed_grid[(x // 2, y // 2)] = "*"
        elif pipe is not None:
            enclosed_grid[(x // 2, y // 2)] = pipe
    # print("---")
    # aoc.print_map(enclosed_grid)
    return sum(1 for x, y, pipe in aoc.iterate_grid(enclosed_grid) if pipe == "*")


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    data = aoc.read_input("input_test_1")
    start, grid = parse(data)
    visited = bfs(start, grid)
    max_distance = max(visited.values())
    t.test_value(max_distance, 4)

    data = aoc.read_input("input_test_2")
    start, grid = parse(data)
    visited = bfs(start, grid)
    max_distance = max(visited.values())
    t.test_value(max_distance, 8)

    data = aoc.read_input("input_test_3")
    start, grid = parse(data)
    t.test_value(find_enclosed(start, grid), 4)

    data = aoc.read_input("input_test_4")
    start, grid = parse(data)
    t.test_value(find_enclosed(start, grid), 8)

    data = aoc.read_input("input_test_5")
    start, grid = parse(data)
    t.test_value(find_enclosed(start, grid), 10)


run_tests(tester)

data = aoc.read_input()
start, grid = parse(data)
visited = bfs(start, grid)

tester.test_section("Part 1")
solution_1 = max(visited.values())
tester.test_solution(solution_1, 7107)

tester.test_section("Part 2")
solution_2 = find_enclosed(start, grid)
tester.test_solution(solution_2, 281)
