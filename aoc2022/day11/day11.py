import typing

import aoc

Monkeys: typing.TypeAlias = list[dict[str, typing.Any]]

tester = aoc.Tester("Monkey in the Middle")


def parse_input(data: str):
    monkeys = []
    for line in data.splitlines():
        if line.startswith("Monkey"):
            monkeys.append({"inspection_count": 0})
        elif not line.strip():
            continue
        else:
            line = line.strip()
            label, value = line.split(":")
            match label:
                case "Starting items":
                    monkeys[-1]["items"] = [int(item) for item in value.split(",")]
                case "Operation":
                    *_, op, value = value.split(" ")
                    value = value if value == "old" else int(value)
                    monkeys[-1]["operation"] = op, value
                case "Test":
                    *_, value = value.split(" ")
                    monkeys[-1]["divisible_by"] = int(value)
                case "If true":
                    *_, monkey = value.split(" ")
                    monkeys[-1]["if_true"] = int(monkey)
                case "If false":
                    *_, monkey = value.split(" ")
                    monkeys[-1]["if_false"] = int(monkey)
                case _:
                    print(f"Not implemented: {label} {value}")
                    print(monkeys[-1])

    lcm = aoc.lcms(*[m["divisible_by"] for m in monkeys])
    for m in monkeys:
        m["lcm"] = lcm
    return monkeys


def chase_the_monkey(monkeys: Monkeys, relief: bool = True):
    for monkey_number, monkey in enumerate(monkeys):
        items = monkey["items"]
        monkey["items"] = []

        for worry_level in items:
            monkey["inspection_count"] += 1

            match monkey["operation"]:
                case "+", "old":
                    worry_level += worry_level
                case "*", "old":
                    worry_level *= worry_level
                case "+", value:
                    worry_level += value
                case "*", value:
                    worry_level *= value
                case _:
                    print(f"Not implemented: {monkey['operation']}")

            if relief:
                worry_level //= 3
            else:
                worry_level %= monkey["lcm"]

            if worry_level % monkey["divisible_by"] == 0:
                receiver_monkey = monkey["if_true"]
            else:
                receiver_monkey = monkey["if_false"]
            monkeys[receiver_monkey]["items"].append(worry_level)
    return monkeys


def play_chase_the_monkey(monkeys: Monkeys, rounds: int, relief: bool = True):
    for i in range(rounds):
        monkeys = chase_the_monkey(monkeys, relief)
    return monkeys


def level_of_monkey_business(input_file: str, rounds: int = 20, relief: bool = True):
    monkeys = parse_input(aoc.read_input(input_file))
    monkeys = play_chase_the_monkey(monkeys, rounds, relief)
    inspections_counts = list(sorted([m["inspection_count"] for m in monkeys]))
    return inspections_counts[-1] * inspections_counts[-2]


tester.test_section("Tests")

test_monkeys = parse_input(aoc.read_input("test_input_1"))
test_monkeys = chase_the_monkey(test_monkeys)

tester.test_value(test_monkeys[0]["items"], [20, 23, 27, 26])
tester.test_value(test_monkeys[1]["items"], [2080, 25, 167, 207, 401, 1046])

test_monkeys = play_chase_the_monkey(test_monkeys, 19)
tester.test_value(test_monkeys[0]["inspection_count"], 101)
tester.test_value(test_monkeys[1]["inspection_count"], 95)
tester.test_value(test_monkeys[2]["inspection_count"], 7)
tester.test_value(test_monkeys[3]["inspection_count"], 105)

tester.test_value(level_of_monkey_business("test_input_1"), 10605)

test_monkeys = parse_input(aoc.read_input("test_input_1"))
test_monkeys = play_chase_the_monkey(test_monkeys, 20, relief=False)

tester.test_value(test_monkeys[0]["inspection_count"], 99)
tester.test_value(test_monkeys[1]["inspection_count"], 97)
tester.test_value(test_monkeys[2]["inspection_count"], 8)
tester.test_value(test_monkeys[3]["inspection_count"], 103)

tester.test_value(level_of_monkey_business("test_input_1", 10000, False), 2713310158)

tester.test_section("Part 1")
tester.test_value(level_of_monkey_business("input"), 112221, "solution to part 1=%s")

tester.test_section("Part 2")
monkey_business = level_of_monkey_business("input", 10000, False)
tester.test_value(monkey_business, 25272176808, "solution to part 2=%s")
# Didn't see the final solution of lcm myself :(
