import aoc

tester = aoc.Tester("Like a Rogue")


def create_row(tiles: str) -> str:
    result = ""
    for index, center in enumerate(tiles):
        left = "." if index == 0 else tiles[index - 1]
        right = "." if index == len(tiles) - 1 else tiles[index + 1]

        match left, center, right:
            case ("^", "^", ".") | (".", "^", "^") | ("^", ".", ".") | (".", ".", "^"):
                result += "^"
            case _:
                result += "."
    return result


def create_rows(tiles: str, count: int = 40) -> list[str]:
    result = [tiles]
    for i in range(count - 1):
        result.append(create_row(result[i]))
    return result


def count_safe_rows(tiles: str, row_count: int) -> int:
    rows = create_rows(tiles, row_count)
    # print("\n".join(rows))
    return len("".join(rows).replace("^", ""))


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    rows = create_rows("..^^.", 3)
    t.test_value(rows[1], ".^^^^")
    t.test_value(rows[2], "^^..^")

    rows = create_rows(".^^.^.^^^^", 3)
    t.test_value(rows[1], "^^^...^..^")
    t.test_value(rows[2], "^.^^.^.^^.")

    t.test_value(count_safe_rows(".^^.^.^^^^", 10), 38)


run_tests(tester)

input_tiles = aoc.read_input()

tester.test_section("Part 1")
tester.test_solution(count_safe_rows(input_tiles, 40), 1961)

tester.test_section("Part 2")
tester.test_solution(count_safe_rows(input_tiles, 400000), 20000795)
# 10s can probably find repeating pattern
