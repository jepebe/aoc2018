import aoc

tester = aoc.Tester("Pyroclastic Flow")

rocks = [
    (1, ((0, 0), (1, 0), (2, 0), (3, 0))),
    (3, ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2))),
    (3, ((2, 0), (2, 1), (0, 2), (1, 2), (2, 2))),
    (4, ((0, 0), (0, 1), (0, 2), (0, 3))),
    (2, ((0, 0), (1, 0), (0, 1), (1, 1))),
]


def move_rock(rock: tuple, direction: tuple[int, int]):
    return tuple(aoc.add_tuple(r, direction) for r in rock)


def crash_rock(chamber: dict[tuple[int, int], str], rock: tuple):
    for r in rock:
        if r in chamber:
            return True
    return False


def add_wall(chamber, level):
    chamber[(-1, level)] = "|"
    chamber[(7, level)] = "|"


def cement_rock(chamber, rock, tallest, symbol="#"):
    for r in rock:
        chamber[r] = symbol
        chamber[(-1, r[1])] = "|"
        chamber[(7, r[1])] = "|"
        if r[1] < tallest:
            tallest = r[1]

    return tallest


def prepare_chamber():
    chamber = {}
    # add floor
    for i in range(7):
        chamber[(i, 0)] = "-"
    for i in range(7):
        add_wall(chamber, -i)
    return chamber


def place_rock(chamber, rock_index, jet_index, jets, tallest):
    (rock_height, rock) = rocks[rock_index % len(rocks)]
    rock = move_rock(rock, (2, (tallest - rock_height - 3)))
    while True:
        jet = jets[jet_index % len(jets)]
        jet_index += 1

        if jet == "<":
            direction = (-1, 0)
        else:
            direction = (1, 0)

        new_rock = move_rock(rock, direction)
        crash = crash_rock(chamber, new_rock)

        if not crash:
            rock = new_rock

        direction = (0, 1)
        new_rock = move_rock(rock, direction)
        crash = crash_rock(chamber, new_rock)

        if not crash:
            rock = new_rock
        else:
            tallest = cement_rock(chamber, rock, tallest)
            break

    for i in range(tallest, tallest - 4, -1):
        add_wall(chamber, i)

    return tallest, jet_index


def chamber_state(chamber, tallest):
    i = 0
    state = 0
    for y in range(tallest, tallest + 30):
        for x in range(7):
            if (x, y) in chamber:
                state = state | (1 << i)
            i += 1
    return state


def drop_rocks(jets: str, rock_count: int):
    chamber = prepare_chamber()

    tallest = 0
    rock_index = 0
    jet_index = 0
    while rock_index < rock_count:
        tallest, jet_index = place_rock(chamber, rock_index, jet_index, jets, tallest)
        rock_index += 1

    return -tallest


def stupid_elephant_rocks(jets: str, rock_count: int):
    chamber = prepare_chamber()

    tallest = 0
    rock_index = 0
    jet_index = 0
    states = {}
    while rock_index < rock_count:
        tallest, jet_index = place_rock(chamber, rock_index, jet_index, jets, tallest)
        rock_index += 1
        state = chamber_state(chamber, tallest)

        memo_key = (rock_index % len(rocks), jet_index % len(jets), state)
        if memo_key in states:
            # cycle found
            cycle_start = states[memo_key][0]
            cycle_start_height = states[memo_key][1]
            cycle_length = rock_index - cycle_start
            height_delta = tallest - states[memo_key][1]

            repeat = (rock_count - cycle_start) // cycle_length
            rest = (rock_count - cycle_start) % cycle_length
            # print(f"{rock_index=} {cycle_start=}, {cycle_length=}, {repeat=}, {rest=}")

            rest_height = 0
            for key, value in states.items():
                if value[0] == cycle_start + rest:
                    rest_height = value[1] - cycle_start_height
                    break

            return -(cycle_start_height + height_delta * repeat + rest_height)
        else:
            states[memo_key] = rock_index, tallest

    return -tallest


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    test_data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    t.test_value(drop_rocks(test_data, 2022), 3068)
    t.test_value(stupid_elephant_rocks(test_data, 2022), 3068)
    t.test_value(stupid_elephant_rocks(test_data, 1000000000000), 1514285714288)


run_tests(tester)

tester.test_section("Part 1")
tester.test_value(drop_rocks(aoc.read_input(), 2022), 3117, "solution to part 1=%s")

tester.test_section("Part 2")
part2 = stupid_elephant_rocks(aoc.read_input(), 1000000000000)
tester.test(part2 != 1548275862086, "too low")
tester.test_value(part2, 1553314121019, "solution to part 2=%s")
