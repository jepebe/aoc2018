import functools
import operator

import aoc

tester = aoc.Tester("Cube Conundrum")


def parse(data: str) -> dict[int, list[dict[str, int]]]:
    games = {}
    for line in data.splitlines():
        game, cube_sets = line.split(":")
        game = int(game[4:])

        games[game] = []
        for cube_set in cube_sets.split(";"):
            cubes = {}
            for subset in cube_set.split(","):
                count, color = subset.strip().split(" ")
                cubes[color] = int(count)

            games[game].append(cubes)

    return games


def check_max_cubes(cubes: list[dict[str, int]], max_counts: dict[str, int]) -> bool:
    for subset in cubes:
        for color, count in subset.items():
            if count > max_counts[color]:
                return False
    return True


def check_all_games(cubes: dict[int, list[dict[str, int]]], max_counts: dict[str, int]) -> int:
    id_sum = 0
    for game, cube_sets in cubes.items():
        if check_max_cubes(cube_sets, max_counts):
            id_sum += game
    return id_sum


def find_max_required_cubes(cubes: list[dict[str, int]]) -> dict[str, int]:
    max_counts = {}
    for subset in cubes:
        for color, count in subset.items():
            if color not in max_counts or count > max_counts[color]:
                max_counts[color] = count
    return max_counts


def find_max_cubes_for_all_games(cubes: dict[int, list[dict[str, int]]]) -> int:
    power = 0
    for game, cube_sets in cubes.items():
        max_counts = find_max_required_cubes(cube_sets)
        power += functools.reduce(operator.mul, max_counts.values())
    return power


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    games = parse(data)

    max_counts = {"red": 12, "green": 13, "blue": 14}
    t.test_value(check_all_games(games, max_counts), 8)

    t.test_value(find_max_cubes_for_all_games(games), 2286)


run_tests(tester)

data = aoc.read_input()

games = parse(data)
max_counts = {"red": 12, "green": 13, "blue": 14}

tester.test_section("Part 1")
tester.test_solution(check_all_games(games, max_counts), 2776)

tester.test_section("Part 2")
tester.test_solution(find_max_cubes_for_all_games(games), 68638)
