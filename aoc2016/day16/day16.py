import aoc

tester = aoc.Tester("Dragon Checksum")

tester.test_section("Tests")


def dragon_curve(initial_state: str) -> str:
    result = []
    result.extend(initial_state)
    result.append("0")
    for v in reversed(initial_state):
        result.append("0" if v == "1" else "1")
    return "".join(result)


tester.test_value(dragon_curve("1"), "100")
tester.test_value(dragon_curve("0"), "001")
tester.test_value(dragon_curve("11111"), "11111000000")
tester.test_value(dragon_curve("111100001010"), "1111000010100101011110000")


def fill_disk(initial_state: str, fill_size: int) -> str:
    fill_data = initial_state
    while len(fill_data) < fill_size:
        fill_data = dragon_curve(fill_data)
    return fill_data[:fill_size]


tester.test_value(fill_disk("1100101101", 12), "110010110100")
tester.test_value(fill_disk("10000", 20), "10000011110010000111")


def checksum(fill_data: str):
    result = fill_data
    while len(result) % 2 == 0:
        new_result = []
        for a, b in aoc.grouper(2, result):
            if a == b:
                new_result.append("1")
            else:
                new_result.append("0")
        result = "".join(new_result)
    return result


tester.test_value(checksum("10000011110010000111"), "01100")


def create_fill_data_checksum(initial_state: str, fill_size: int) -> str:
    fill = fill_disk(initial_state, fill_size)
    return checksum(fill)


tester.test_value(create_fill_data_checksum("10000", 20), "01100")

tester.test_section("Part 1")
part_1 = create_fill_data_checksum("10010000000110000", 272)
tester.test_value(part_1, "10010110010011110", "solution to part 1=%s")

tester.test_section("Part 2")
part_2 = create_fill_data_checksum("10010000000110000", 35651584)
tester.test_value(part_2, "01101011101100011", "solution to part 2=%s")
