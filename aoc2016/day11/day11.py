import heapq
import itertools

import aoc

tester = aoc.Tester("Radioisotope Thermoelectric Generators")


def done(floors: tuple) -> bool:
    return len(floors[0]) == 0 and len(floors[1]) == 0 and len(floors[2]) == 0


def safe(floor: tuple) -> bool:
    generators = set(i for i in floor if i.endswith("G"))
    for item in floor:
        if item[-1:] == "M":
            if item[:-1] + "G" in generators:
                # Safe combo
                continue
            elif len(generators) > 0:
                return False
    return True


def alternatives(f, floors) -> []:
    alts = []
    for a, b in itertools.combinations_with_replacement(floors[f], 2):
        current_floor = tuple(sorted(i for i in floors[f] if i != a and i != b))
        # print(a, b, floors[f], current_floor)
        if not safe(current_floor):
            continue

        if a[-1:] != b[-1:] and a[:-1] != b[:-1]:
            # mismatch between generator and microchip
            # print(f"{a} mismatch with {b}")
            continue

        if a == b:
            move = (a,)
        else:
            move = (a, b)

        if f < 3:
            new_floors = [floors[0], floors[1], floors[2], floors[3]]
            new_floors[f] = current_floor
            new_floors[f + 1] = tuple(sorted(new_floors[f + 1] + move))

            if safe(new_floors[f + 1]):
                alts.append((f + 1, tuple(new_floors)))

        if f > 0:
            new_floors = [floors[0], floors[1], floors[2], floors[3]]
            new_floors[f] = current_floor
            new_floors[f - 1] = tuple(sorted(new_floors[f - 1] + move))
            if safe(new_floors[f - 1]):
                alts.append((f - 1, tuple(new_floors)))
    return alts


def move_to_top_floor(floors: tuple) -> int:
    queue = [(0, 0, floors)]
    visited = set()
    while queue:
        # t for time, f for current floor, floors is layout
        t, f, floors = heapq.heappop(queue)
        # print(f"{t} {f} {floors}")
        if done(floors):
            return t

        for nf, new_floors in alternatives(f, floors):
            next_move = (t + 1, nf, new_floors)
            fingerprint = []
            for floor in new_floors:
                g = sum(1 for i in floor if i.endswith("G"))
                m = sum(1 for i in floor if i.endswith("M"))
                fingerprint.append((g, m))
            fingerprint = (t + 1, nf, tuple(fingerprint))

            if fingerprint not in visited:
                visited.add(fingerprint)
                queue.append(next_move)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    test_floors = (
        ("HM", "LM"),
        ("HG",),
        ("LG",),
        ()
    )

    t.test_value(move_to_top_floor(test_floors), 11)


run_tests(tester)

input_floors = (
    ("PmG", "PmM"),
    ("CoG", "CmG", "RuG", "PuG"),
    ("CoM", "CmM", "RuM", "PuM"),
    ()
)

tester.test_section("Part 1")
tester.test_solution(move_to_top_floor(input_floors), 33)

input_floors = (
    ("PmG", "PmM", "ElG", "ElM", "DiG", "DiM"),
    ("CoG", "CmG", "RuG", "PuG"),
    ("CoM", "CmM", "RuM", "PuM"),
    ()
)

tester.test_section("Part 2")
tester.test_solution(move_to_top_floor(input_floors), 57)
