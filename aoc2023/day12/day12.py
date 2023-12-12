import aoc

tester = aoc.Tester("Hot Springs")


def parse(data: str) -> list[tuple[str, list[int]]]:
    spring_list = []
    for line in data.splitlines():
        springs, crc = line.split(" ")
        crc = list(map(int, crc.split(",")))
        spring_list.append((springs, crc))
        # print(springs, crc)

    return spring_list


def find_combos(memo: dict, springs: str, crc: list[int], current: str = "", group: int = 0) -> int:
    # if current == "":
    #     print(springs, crc)

    if current in memo:
        return memo[current]

    if len(current) == len(springs):
        variant = current.replace(".", " ").split()

        if len(crc) != len(variant):
            return 0

        variant = list(map(len, variant))
        if crc == variant:
            return 1
        return 0

    if springs[len(current)] == "?":
        dot = find_combos(memo, springs, crc, current + ".")
        octothorpe = find_combos(memo, springs, crc, current + "#")
        memo[current] = dot + octothorpe
        return dot + octothorpe
    else:
        return find_combos(memo, springs, crc, current + springs[len(current)])




# def find_combos(springs: str, crc: int, current: str) -> int:
#     if len(current) == len(springs):
#
#         variant = current.replace(".", " ").split()
#         variant = list(map(len, variant))
#         if len(variant) == 1 and crc == variant[0]:
#             return 1
#         return 0
#
#     if springs[len(current)] == "?":
#         return find_combos(springs, crc, current + ".") + find_combos(springs, crc, current + "#")
#     else:
#         return find_combos(springs, crc, current + springs[len(current)])


# def find_combos_2(springs: str, crc: list[int], memo: dict) -> int:
#     if springs in memo:
#         return 0
#
#     spring_list = springs.replace(".", " ").split()
#     if len(spring_list) == len(crc):
#         combos = 1
#         for spring, group in zip(spring_list, crc):
#             if len(spring) < group:
#                 # print("unpossible")
#                 return 0  # this split is not possible
#             if len(spring) == group:
#                 combos *= 1
#             if len(spring) > group:
#                 if (spring, group) in big_memo:
#                     cmb = big_memo[(spring, group)]
#                 else:
#                     cmb = find_combos(spring, group, "")
#                     if (spring, group) not in big_memo:
#                         big_memo[(spring, group)] = cmb
#                 combos *= cmb
#
#         memo[springs] = combos
#         print(springs, crc, combos)
#         return combos
#
#     else:
#         combos = 0
#         for split in range(1, len(springs) - 1):
#             if springs[split] == "?":
#                 new_springs = springs[:split] + "." + springs[split + 1:]
#                 combos += find_combos_2(new_springs, crc, memo)
#         return combos


def find_combos_unfolded(springs: str, crc: list[int]) -> int:
    springs = "?".join([springs for _ in range(5)])
    return find_combos(springs, crc * 5, "")


def find_all_combos(springs: list[tuple[str, list[int]]]) -> int:
    total = 0
    for spring in springs:
        total += find_combos({}, spring[0], spring[1])
    return total


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    springs = parse(data)

    t.test_value(find_combos({}, springs[0][0], springs[0][1]), 1)
    t.test_value(find_combos({}, springs[1][0], springs[1][1]), 4)
    t.test_value(find_combos({}, springs[2][0], springs[2][1]), 1)
    t.test_value(find_combos({}, springs[3][0], springs[3][1]), 1)
    t.test_value(find_combos({}, springs[4][0], springs[4][1]), 4)
    t.test_value(find_combos({}, springs[5][0], springs[5][1]), 10)

    t.test_value(find_all_combos(springs), 21)

    # t.test_value(find_combos_unfolded(springs[0][0], springs[0][1]), 1)
    # t.test_value(find_combos_unfolded(springs[1][0], springs[1][1]), 16384)


run_tests(tester)

data = aoc.read_input()
springs = parse(data)

tester.test_section("Part 1")
solution_1 = find_all_combos(springs)
tester.test_solution(solution_1, 6949)

tester.test_section("Part 2")
tester.test_solution(2, 208191)
