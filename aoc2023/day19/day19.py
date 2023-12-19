import aoc

tester = aoc.Tester("Aplenty")

Rating = dict[str, aoc.Range]
Workflows = dict[str, callable]


def accept_or_reject(workflow: str) -> callable:
    def f(workflows: Workflows, ratings: Rating, accepted: list, path: str) -> int:
        if workflow == "A":
            combinations = 1
            for rating in ratings.values():
                combinations *= len(rating)

            # print(path, combinations)
            # print_rating_range([ratings])

            if combinations > 0:
                accepted.append(ratings)
            return combinations
        elif workflow == "R":
            return 0
        else:
            raise ValueError(f"Invalid workflow: {workflow}")

    return f


def workflow_expr(workflow: str) -> callable:
    def f(workflows: Workflows, ratings: Rating, accepted: list, path: str) -> int:
        return workflows[workflow](
            workflows, ratings, accepted, f"{path} -> {workflow}"
        )

    return f


def compare(category: str, value: int, comparator: str) -> callable:
    def f(ratings: Rating) -> tuple[Rating, Rating]:
        true_range = aoc.Range(0, 0)
        false_range = aoc.Range(0, 0)

        r = ratings[category]
        if comparator == "<":
            # with less than, the low end of the range is the true range
            if value in r:
                true_range = aoc.Range(r.start, value)
                false_range = aoc.Range(value, r.end)
            elif r.end <= value:
                true_range = r
            else:
                false_range = r

        elif comparator == ">":
            # with greater than, the high end of the range is the true range
            if value in r:
                false_range = aoc.Range(r.start, value + 1)
                true_range = aoc.Range(value + 1, r.end)
            elif r.end < value:
                false_range = r
            else:
                true_range = r

        true_rating = {c: r for c, r in ratings.items()}
        true_rating[category] = true_range
        false_rating = {c: r for c, r in ratings.items()}
        false_rating[category] = false_range
        return true_rating, false_rating

    return f


def conditional_expr(conditional, true_action, false_action) -> callable:
    def f(workflows: Workflows, ratings: Rating, accepted: list, path: str) -> int:
        true_ratings, false_ratings = conditional(ratings)

        result = true_action(workflows, true_ratings, accepted, path)
        result += false_action(workflows, false_ratings, accepted, path)
        return result

    return f


def parse_workflow(workflow: str) -> callable:
    workflow = workflow.strip()
    if workflow in "AR":
        return accept_or_reject(workflow)
    elif workflow.isalpha():
        return workflow_expr(workflow)

    index = workflow.index(":")
    cond, actions = workflow[:index], workflow[index + 1 :]
    if "<" in cond:
        index = cond.index("<")
    else:
        index = cond.index(">")
    category = cond[:index]
    value = cond[index + 1 :]
    cond_expr = compare(category, int(value), cond[index])
    index = actions.index(",")
    true_action = parse_workflow(actions[:index])
    false_action = parse_workflow(actions[index + 1 :])
    return conditional_expr(cond_expr, true_action, false_action)


def parse(data: str) -> tuple[Workflows, list[dict[str, int]]]:
    rating_mode = False
    workflows = {}
    rating_list = []
    for line in data.splitlines():
        if line == "":
            rating_mode = True
            continue

        if not rating_mode:
            name = line[: line.index("{")]
            workflow = line[line.index("{") + 1 : line.index("}")]
            workflows[name] = parse_workflow(workflow)
        else:
            rating = line[1:-1].split(",")
            ratings = {}
            for r in rating:
                r = r.split("=")
                ratings[r[0]] = int(r[1])
            rating_list.append(ratings)

    return workflows, rating_list


def rating_is_valid(rating: dict[str, int], valid_ranges: dict[str, aoc.Range]):
    valid = rating["x"] in valid_ranges["x"]
    valid = valid and rating["m"] in valid_ranges["m"]
    valid = valid and rating["a"] in valid_ranges["a"]
    valid = valid and rating["s"] in valid_ranges["s"]
    return valid


def process(workflows: Workflows, ratings: list[dict[str, int]]) -> int:
    rating_ranges = {
        "x": aoc.Range(1, 4001),
        "m": aoc.Range(1, 4001),
        "a": aoc.Range(1, 4001),
        "s": aoc.Range(1, 4001),
    }
    accepted = []
    _ = workflows["in"](workflows, rating_ranges, accepted, "in")

    valid_ratings = []
    for rating in ratings:
        for valid_ranges in accepted:
            if rating_is_valid(rating, valid_ranges):
                valid_ratings.append(rating)
                break

    return sum(sum(rating.values()) for rating in valid_ratings)


def process_ranges(workflows: Workflows) -> int:
    ratings = {
        "x": aoc.Range(1, 4001),
        "m": aoc.Range(1, 4001),
        "a": aoc.Range(1, 4001),
        "s": aoc.Range(1, 4001),
    }
    accepted = []
    result = workflows["in"](workflows, ratings, accepted, "in")

    # print_rating_range(accepted)
    return result


def print_rating_range(rating_range):
    for rating in rating_range:
        for category in "xmas":
            r = rating[category]
            print(f"{category}: [{r.start:4d} - {r.end:4d}]", end=" ")
        print()


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    workflows, ratings = parse(data)

    t.test_value(process(workflows, ratings), 19114)
    t.test_value(process_ranges(workflows), 167409079868000)


run_tests(tester)

data = aoc.read_input()
workflows, ratings = parse(data)

tester.test_section("Part 1")
solution_1 = process(workflows, ratings)
tester.test_solution(solution_1, 575412)

tester.test_section("Part 2")
solution_2 = process_ranges(workflows)
tester.test_solution(solution_2, 126107942006821)
