import math

import aoc

tester = aoc.Tester("Monkey Math")


def parse_input(filename: str) -> dict:
    data = aoc.read_input(filename)
    expressions = {}
    for line in data.splitlines():
        key, expression = line.split(sep=":")
        try:
            expressions[key] = int(expression)
        except ValueError:
            k1, op, k2 = expression.strip().split(sep=" ")
            expressions[key] = (k1, op, k2)
    return expressions


def refine_expression(calc, exp):
    refinements = 0
    for key, value in exp.items():
        if key in calc:
            continue

        match value:
            case int(v):
                calc[key] = v
            case (k1, "*", k2):
                if k1 in calc and k2 in calc:
                    calc[key] = calc[k1] * calc[k2]
                    refinements += 1
            case (k1, "+", k2):
                if k1 in calc and k2 in calc:
                    calc[key] = calc[k1] + calc[k2]
                    refinements += 1
            case (k1, "-", k2):
                if k1 in calc and k2 in calc:
                    calc[key] = calc[k1] - calc[k2]
                    refinements += 1
            case (k1, "/", k2):
                if k1 in calc and k2 in calc:
                    calc[key] = calc[k1] / calc[k2]
                    refinements += 1
    return refinements


def calculate_expression(exp: dict) -> int:
    calc = {}
    while "root" not in calc:
        refine_expression(calc, exp)

    return calc["root"]


def calculate_human_expression(exp: dict) -> tuple[bool, int, int]:
    eq1, _, eq2 = exp["root"]
    calc = {}
    while eq1 not in calc or eq2 not in calc:
        refine_expression(calc, exp)

    return calc[eq1] == calc[eq2], calc[eq1], calc[eq2]


def find_human_number(exp: dict):
    exp["humn"] = 2
    _, k1, k2 = calculate_human_expression(exp)

    sign = math.copysign(1, k1 - k2)

    lower_bound = 0
    while sign == math.copysign(1, k1 - k2):  # continue until the sign switches
        lower_bound = exp["humn"]
        exp["humn"] += exp["humn"]
        _, k1, k2 = calculate_human_expression(exp)
    upper_bound = exp["humn"]

    tester.peek_delta_time(f"Lower bound {lower_bound} upper bound {upper_bound}")

    eq = False
    while not eq:
        mid = lower_bound + (upper_bound - lower_bound) // 2
        exp["humn"] = mid
        eq, k1, k2 = calculate_human_expression(exp)

        if sign == math.copysign(1, k1 - k2):  # sign is the same -> too low
            lower_bound = mid
        else:  # sign has switched -> too high
            upper_bound = mid

    return exp["humn"]


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    t.test_value(calculate_expression(parse_input("test_input")), 152)
    t.test_value(find_human_number(parse_input("test_input")), 301)


run_tests(tester)

tester.test_section("Part 1")
tester.test_value(calculate_expression(parse_input("input")), 22382838633806, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_human_number(parse_input("input")), 3099532691300, "solution to part 2=%s")
