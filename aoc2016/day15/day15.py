import aoc

tester = aoc.Tester("Timing is Everything")

test_disc_data = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""


def parse_discs(data: str):
    discs = []
    for line in data.split(sep="\n"):
        elements = line.split(sep=" ")
        sides = int(elements[3])
        pos = int(elements[11].replace(".", ""))
        discs.append((sides, pos))
    return discs


test_discs = parse_discs(test_disc_data)
tester.test_value(test_discs, [(5, 4), (2, 1)])


def iterate(discs):
    for index, (s, p) in enumerate(discs):
        p = (p + 1) % s
        discs[index] = (s, p)
    return discs


def check_configuration(discs):
    for index, (s, p) in enumerate(discs, start=1):
        if (p + index) % s != 0:
            return False
    return True


def find_solution(discs):
    iterations = 0
    while not check_configuration(discs):
        discs = iterate(discs)
        iterations += 1
    return iterations


tester.test(not check_configuration(discs=test_discs))
tester.test_value(find_solution(test_discs), 5)

with open("input") as f:
    data = f.read()

discs = parse_discs(data)

tester.test_section("Part 1")
tester.test_value(find_solution(list(discs)), 376777, "solution to part 1=%s")

discs.append((11, 0))

tester.test_section("Part 2")
tester.test_value(find_solution(list(discs)), 3903937, "solution to part 2=%s")
