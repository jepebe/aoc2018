import hashlib

import aoc

UP = (0, -1, "U")
DOWN = (0, 1, "D")
LEFT = (-1, 0, "L")
RIGHT = (1, 0, "R")

tester = aoc.Tester("Two Steps Forward")


def find_neighbors(x, y, code: str):
    neighbors = []
    doors = hashlib.md5(bytes(code.encode("utf8"))).hexdigest()
    for index, (dx, dy, d) in enumerate([UP, DOWN, LEFT, RIGHT]):
        nx = x + dx
        ny = y + dy

        if 0 <= nx < 4 and 0 <= ny < 4 and doors[index] in "bcdef":
            neighbors.append((nx, ny, code + d))
    return neighbors


def find_path(door_code: str) -> tuple[str, int]:
    solutions = []
    queue = [(0, 0, door_code)]

    while len(queue) > 0:
        x, y, code = queue.pop(0)

        if x == 3 and y == 3:
            solutions.append((x, y,  code[len(door_code):]))
            continue

        neighbors = find_neighbors(x, y, code)
        for (nx, ny, ncode) in neighbors:
            queue.append((nx, ny, ncode))

    longest = max([len(code) for _, _, code in solutions])
    return solutions[0][2], longest


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    ihgpwlah = find_path("ihgpwlah")
    t.test_value(ihgpwlah[0], "DDRRRD")
    t.test_value(ihgpwlah[1], 370)
    kglvqrro = find_path("kglvqrro")
    t.test_value(kglvqrro[0], "DDUDRLRRUDRD")
    t.test_value(kglvqrro[1], 492)
    ulqzkmiv = find_path("ulqzkmiv")
    t.test_value(ulqzkmiv[0], "DRURDRUDDLLDLUURRDULRLDUUDDDRR")
    t.test_value(ulqzkmiv[1], 830)


run_tests(tester)

tester.test_section("Part 1")
udskfozm = find_path("udskfozm")
tester.test_solution(udskfozm[0], "DDRLRRUDDR")

tester.test_section("Part 2")
tester.test_solution(udskfozm[1], 556)
