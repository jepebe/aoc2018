import aoc

tester = aoc.Tester("Lavaduct Lagoon")


def parse(data: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    points = [(0, 0)]
    colors = [(0, 0)]

    x, y = 0, 0
    cx, cy = 0, 0
    for line in data.splitlines():
        direction, steps, color = line.split()
        steps = int(steps)

        match direction:
            case "R":
                x += steps
            case "L":
                x -= steps
            case "U":
                y -= steps
            case "D":
                y += steps
            case _:
                raise ValueError(f"Invalid direction: {direction}")
        points.append((x, y))

        steps, direction = int(color[2:7], base=16), int(color[7:8])
        match direction:
            case 0:  # right
                cx += steps
            case 1:  # down
                cy += steps
            case 2:  # left
                cx -= steps
            case 3:  # up
                cy -= steps
            case _:
                raise ValueError(f"Invalid direction: {direction}")

        colors.append((cx, cy))
    return points, colors


def shoelace(points: list[tuple[int, int]]) -> int:
    # shoelace formula
    area = 0
    boundary = 0
    for i in range(len(points) - 1):
        x_i = points[i][0]
        y_i = points[i][1]
        x_i1 = points[i + 1][0]
        y_i1 = points[i + 1][1]
        area += x_i * y_i1 - x_i1 * y_i
        boundary += abs(x_i1 - x_i) + abs(y_i1 - y_i)

    area = abs(area) / 2

    # picks theorem
    interior = area + boundary / 2 + 1  # do not understand +1 instead of -1 here ¯\_(ツ)_/¯

    # Reddit explanation:
    # - The formula given on the Wiki page needs some manipulation.
    #   Pick's theorem says that A = i + b / 2 - 1, where A is the area of the
    #   polygon, i is the number of internal integer points, and b is the number of
    #   boundary integer points.
    # - We have Area from the Shoelace Formula, and we have the number of boundary
    #   points with the perimeter. We want the internal points, so we have some algebra to do.
    # - Solve for i by subtracting b/2 - 1 from both sides, getting i = A - b / 2 + 1.
    #   Note from the given example that you can get the number of enclosed points
    #   with just this formula. But we have a little more work to do.
    # - Add the perimeter, since those boundary points are also counted.
    #   Thus, our formula is A - b / 2 + 1 + b = A + b / 2 + 1

    return int(interior)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    points, colors = parse(aoc.read_input("input_test"))
    t.test_value(shoelace([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]), 9)
    t.test_value(shoelace(points), 62)

    t.test_value(shoelace(colors), 952408144115)


run_tests(tester)

points, colors = parse(aoc.read_input())

tester.test_section("Part 1")
solution_1 = shoelace(points)
tester.test_value_neq(solution_1, 50266)
tester.test_solution(solution_1, 50603)

tester.test_section("Part 2")
solution_2 = shoelace(colors)
tester.test_less_than(solution_2, 259667436989233)
tester.test_greater_than(solution_2, 96556165374331)
tester.test_solution(solution_2, 96556251590677)
