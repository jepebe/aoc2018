import dataclasses
import re
import typing

import aoc

Vec2: typing.TypeAlias = tuple[int, int]

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

tester = aoc.Tester("Monkey Map")


def parse_input(filename: str):
    data = aoc.read_input(filename)
    grid = {}
    extents = {}

    path = None
    y = 1
    start_pos = None
    for line in data.splitlines():
        x = 1
        if not line:
            continue

        if "0" <= line[0] <= "9":
            path = line
            break

        for c in line:
            if c != " ":
                grid[(x, y)] = c

                if f"r{y}" not in extents:
                    extents[f"r{y}"] = [x, x]
                else:
                    extents[f"r{y}"][1] = x

                if f"c{x}" not in extents:
                    extents[f"c{x}"] = [y, y]
                else:
                    extents[f"c{x}"][1] = y

                if not start_pos:
                    start_pos = (x, y)
            x += 1
        y += 1

    pointers = {}
    for rc, ext in extents.items():
        if rc.startswith("r"):
            row = int(rc[1:])
            pointers[(2, ext[0], row)] = (2, (ext[1], row))
            pointers[(0, ext[1], row)] = (0, (ext[0], row))
        else:
            col = int(rc[1:])
            pointers[(3, col, ext[0])] = (3, (col, ext[1]))
            pointers[(1, col, ext[1])] = (1, (col, ext[0]))

    return grid, pointers, start_pos, re.split("([R|L])", path)


def walk_path(grid: dict, pointers: dict, path: list, start: Vec2):
    # move_map = dict(grid)
    pos = start
    facing = 0
    for op in path:
        match op:
            case "R":
                facing = (facing + 1) % 4
            case "L":
                facing = (facing - 1) % 4
            case steps:
                for _ in range(int(steps)):
                    # match DIRECTIONS[facing]:
                    #     case (1, 0):
                    #         move_map[pos] = ">"
                    #     case (-1, 0):
                    #         move_map[pos] = "<"
                    #     case (0, 1):
                    #         move_map[pos] = "v"
                    #     case (0, -1):
                    #         move_map[pos] = "^"

                    next_pos = aoc.add_tuple(pos, DIRECTIONS[facing])
                    new_facing = facing
                    if next_pos not in grid:
                        new_facing, next_pos = pointers[(facing, *pos)]

                    match grid[next_pos]:
                        case ".":
                            pos = next_pos
                            facing = new_facing
                        case "#":
                            pass
                        case _:
                            assert False, f"Unknown map value {_}"

    # aoc.print_map(move_map)
    return pos[1] * 1000 + pos[0] * 4 + facing


def create_tile(grid: dict, start: Vec2, tile_size: int = 4):
    data = {}

    for y in range(tile_size):
        for x in range(tile_size):
            pos = aoc.add_tuple(start, (x, y))
            data[pos] = grid[pos]

    tile = {
        "start": start,
        "end": pos,
        "data": data,
    }
    return tile


def split_grid(grid: dict, tile_size: int = 4) -> dict[tuple[int, int], dict]:
    tiles = {}
    for j in range(4):
        for i in range(4):
            pos = (i * tile_size + 1, j * tile_size + 1)
            if pos in grid:
                tile = create_tile(grid, pos, tile_size)
                tiles[(i, j)] = tile

    # for tile in tiles.values():
    #     aoc.print_map(tile["data"])
    #     print(tile)

    return tiles


def monkey_path(filename: str) -> int:
    grid, extents, start, path = parse_input(filename)
    return walk_path(grid, extents, path, start)


@dataclasses.dataclass
class Edge:
    facing: int
    tile_id: tuple[int, int]
    direction: int  # if negative go in reverse direction


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


def edge_points(tiles: dict[Vec2, dict], t: Edge) -> tuple[Vec2, Vec2]:
    t_start = tiles[t.tile_id]["start"]
    t_end = tiles[t.tile_id]["end"]

    match t.facing, t.direction:
        case 0, 1:  # right
            start = t_end[0], t_start[1]
            # end = t_end
            direction = (0, 1)
        case 0, -1:  # right, reversed
            start = t_end
            # end = t_end[0], t_start[1]
            direction = (0, -1)
        case 1, 1:  # down
            start = t_start[0], t_end[1]
            # end = t_end
            direction = (1, 0)
        case 1, -1:  # down, reversed
            start = t_end
            # end = t_start[0], t_end[1]
            direction = (-1, 0)
        case 2, 1:  # right
            start = t_start
            # end = t_start[0], t_end[1]
            direction = (0, 1)
        case 2, -1:  # right, reversed
            start = t_start[0], t_end[1]
            # end = t_start
            direction = (0, -1)
        case 3, 1:  # up
            start = t_start
            # end = t_end[0], t_start[1]
            direction = (1, 0)
        case 3, -1:  # up, reversed
            start = t_end[0], t_start[1]
            # end = t_start
            direction = (-1, 0)
        case _:
            assert False, f"Unhandled state {t.facing} {t.direction}"
    return start, direction


def connect_tiles(tiles: dict[Vec2, dict], t1: Edge, t2: Edge, tile_size: int):
    pointers = {}

    t1_pos, t1_direction = edge_points(tiles, t1)
    t2_pos, t2_direction = edge_points(tiles, t2)

    for i in range(tile_size):
        pointers[(t1.facing, t1_pos[0], t1_pos[1])] = ((t2.facing + 2) % 4, t2_pos)
        pointers[(t2.facing, t2_pos[0], t2_pos[1])] = ((t1.facing + 2) % 4, t1_pos)
        t1_pos = aoc.add_tuple(t1_pos, t1_direction)
        t2_pos = aoc.add_tuple(t2_pos, t2_direction)
    return pointers


def monkey_cube_path(filename: str, tile_size: int = 4) -> int:
    grid, _, start, path = parse_input(filename)
    tiles = split_grid(grid, tile_size=tile_size)

    pointers = {}
    if tile_size == 4:
        pointers |= connect_tiles(tiles, Edge(UP, (1, 1), 1), Edge(LEFT, (2, 0), 1), tile_size=tile_size)
        pointers |= connect_tiles(tiles, Edge(DOWN, (1, 1), 1), Edge(LEFT, (2, 2), -1), tile_size=tile_size)

        pointers |= connect_tiles(tiles, Edge(RIGHT, (2, 0), 1), Edge(RIGHT, (3, 2), -1), tile_size=tile_size)
        pointers |= connect_tiles(tiles, Edge(UP, (2, 0), 1), Edge(UP, (0, 1), -1), tile_size=tile_size)

        pointers |= connect_tiles(tiles, Edge(DOWN, (2, 2), 1), Edge(DOWN, (0, 1), -1), tile_size=tile_size)

        pointers |= connect_tiles(tiles, Edge(DOWN, (3, 2), 1), Edge(LEFT, (0, 1), -1), tile_size=tile_size)
        pointers |= connect_tiles(tiles, Edge(UP, (3, 2), -1), Edge(RIGHT, (2, 1), 1), tile_size=tile_size)
    else:
        pointers |= connect_tiles(tiles, Edge(UP, (1, 0), 1), Edge(LEFT, (0, 3), 1), tile_size=tile_size)
        pointers |= connect_tiles(tiles, Edge(LEFT, (1, 0), 1), Edge(LEFT, (0, 2), -1), tile_size=tile_size)

        pointers |= connect_tiles(tiles, Edge(RIGHT, (1, 1), 1), Edge(DOWN, (2, 0), 1), tile_size=tile_size)
        pointers |= connect_tiles(tiles, Edge(LEFT, (1, 1), 1), Edge(UP, (0, 2), 1), tile_size=tile_size)

        pointers |= connect_tiles(tiles, Edge(RIGHT, (1, 2), 1), Edge(RIGHT, (2, 0), -1), tile_size=tile_size)
        pointers |= connect_tiles(tiles, Edge(DOWN, (1, 2), 1), Edge(RIGHT, (0, 3), 1), tile_size=tile_size)

        pointers |= connect_tiles(tiles, Edge(UP, (2, 0), 1), Edge(DOWN, (0, 3), 1), tile_size=tile_size)

    return walk_path(grid, pointers, path, start)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    t.test_value(monkey_path("test_input"), 6032)

    t.test_value(monkey_cube_path("test_input"), 5031)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_solution(monkey_path("input"), 47462)

tester.test_section("Part 2")
part2 = monkey_cube_path("input", tile_size=50)
tester.test_greater_than(part2, 122152)
tester.test_solution(part2, 137045)
