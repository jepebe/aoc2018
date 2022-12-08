import functools
import operator

import aoc

Grid = dict[tuple[int, int], int]

tester = aoc.Tester("Treetop Tree House")

tester.test_section("Tests")

test_data = """30373
25512
65332
33549
35390"""


def parse_input(data: str) -> Grid:
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, tree in enumerate(line):
            grid[(x, y)] = int(tree)

    # aoc.print_map(grid, func=lambda g, p: str(g[p]))
    return grid


def is_tree_visible(x: int, y: int, grid: Grid, extents: aoc.Extents):
    if x == 0 or y == 0 or x == extents[1] or y == extents[3]:
        return True, 0

    tree_size = grid[x, y]

    visible = [True, True, True, True]
    score = [0, 0, 0, 0]

    for column in range(x - 1, 0 - 1, -1):
        score[0] += 1
        if grid[column, y] >= tree_size:
            visible[0] = False
            break

    for column in range(x + 1, extents[1] + 1):
        score[1] += 1
        if grid[column, y] >= tree_size:
            visible[1] = False
            break

    for row in range(y - 1, 0 - 1, -1):
        score[2] += 1
        if grid[x, row] >= tree_size:
            visible[2] = False
            break

    for row in range(y + 1, extents[3] + 1):
        score[3] += 1
        if grid[x, row] >= tree_size:
            visible[3] = False
            break

    return any(visible), functools.reduce(operator.mul, score)


def count_visible_trees(grid: Grid) -> tuple[int, int]:
    new_grid = {}
    extents = aoc.find_extents(grid)
    columns = extents[1] + 1
    rows = extents[3] + 1

    for y in range(0, rows):
        for x in range(0, columns):
            new_grid[x, y] = is_tree_visible(x, y, grid, extents)

    # aoc.print_map(new_grid)
    visible_count = sum([1 for visible, _ in new_grid.values() if visible])
    max_score = max([score for _, score in new_grid.values()])
    return visible_count, max_score


test_grid = parse_input(test_data)
tester.test_value(count_visible_trees(test_grid)[0], 21)
tester.test_value(count_visible_trees(test_grid)[1], 8)

grid = parse_input(aoc.read_input())

tester.test_section("Part 1")
tester.test_value(count_visible_trees(grid)[0], 1814, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(count_visible_trees(grid)[1], 330786, "solution to part 2=%s")
