import aoc

tester = aoc.Tester("The Floor Will Be Lava")


def parse(data: str):
    grid: aoc.Grid2D = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    return grid


north = (0, -1)
south = (0, 1)
east = (1, 0)
west = (-1, 0)


def bounce(
        grid: aoc.Grid2D,
        start: tuple[int, int] = (0, 0),
        start_dir: tuple[int, int] = (1, 0),
) -> int:
    queue = [(start, start_dir)]
    new_grid = {}
    while queue:
        pos, direction = queue.pop()
        if pos not in grid:
            continue

        if pos in new_grid:
            if direction in new_grid[pos]:
                # we've already been here and gone this direction
                continue
            new_grid[pos].append(direction)
        else:
            new_grid[pos] = [direction]

        tile = grid[pos]
        match tile, direction:
            case ".", _:
                queue.append((aoc.add_tuple(pos, direction), direction))
            case ("|", (0, 1)) | ("|", (0, -1)):
                queue.append((aoc.add_tuple(pos, direction), direction))
            case ("|", (1, 0)) | ("|", (-1, 0)):
                queue.append((aoc.add_tuple(pos, north), north))
                queue.append((aoc.add_tuple(pos, south), south))
            case ("-", (1, 0)) | ("-", (-1, 0)):
                queue.append((aoc.add_tuple(pos, direction), direction))
            case ("-", (0, 1)) | ("-", (0, -1)):
                queue.append((aoc.add_tuple(pos, east), east))
                queue.append((aoc.add_tuple(pos, west), west))
            case ("/", d):
                direction = (-d[1], -d[0])  # rotate 90 degrees CCW
                queue.append((aoc.add_tuple(pos, direction), direction))
            case ("\\", d):
                direction = (d[1], d[0])  # rotate 90 degrees CW
                queue.append((aoc.add_tuple(pos, direction), direction))
            case _, _:
                raise ValueError(f"Unknown tile {tile} {direction}")

    return len(new_grid.values())


def find_maximum_energizement(grid: aoc.Grid2D) -> int:
    minx, maxx, miny, maxy = aoc.find_extents(grid)
    assert maxx == maxy
    max_energizement = 0
    for i in range(minx, maxx + 1):
        energizement = bounce(grid, (i, 0), south)
        if energizement > max_energizement:
            max_energizement = energizement

        energizement = bounce(grid, (i, maxy), north)
        if energizement > max_energizement:
            max_energizement = energizement

        energizement = bounce(grid, (0, i), east)
        if energizement > max_energizement:
            max_energizement = energizement

        energizement = bounce(grid, (maxx, i), west)
        if energizement > max_energizement:
            max_energizement = energizement
    return max_energizement


def directionizer(grid: aoc.Grid2D, pos: tuple[int, int]) -> str:
    # support function for printing
    if pos not in grid:
        return "."

    directions = grid[pos]
    if len(directions) == 1:
        match directions[0]:
            case (0, 1):
                return "v"
            case (0, -1):
                return "^"
            case (1, 0):
                return ">"
            case (-1, 0):
                return "<"
            case _:
                print(f"Unknown direction {directions[0]}")
    else:
        return str(len(directions))


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    grid = parse(aoc.read_input("input_test"))

    t.test_value(bounce(grid), 46)

    t.test_value(find_maximum_energizement(grid), 51)


run_tests(tester)

data = aoc.read_input()
grid = parse(data)

tester.test_section("Part 1")
tester.test_solution(bounce(grid), 7472)

tester.test_section("Part 2")
tester.test_solution(find_maximum_energizement(grid), 7716)
