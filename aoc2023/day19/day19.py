from pprint import pprint

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


def less_than(category: str, value: int) -> callable:
    def f(ratings: Rating) -> tuple[Rating, Rating]:
        gte = aoc.Range(0, 0)
        lt = aoc.Range(0, 0)

        r = ratings[category]
        if value in r:
            lt = aoc.Range(r.start, value)
            gte = aoc.Range(value, r.end)
        elif r.end <= value:
            lt = r
        else:
            gte = r

        lt_rating = {c: r for c, r in ratings.items()}
        lt_rating[category] = lt
        gte_rating = {c: r for c, r in ratings.items()}
        gte_rating[category] = gte
        return lt_rating, gte_rating

    return f


def greater_than(category: str, value: int) -> callable:
    def f(ratings: Rating) -> tuple[Rating, Rating]:
        gt = aoc.Range(0, 0)
        lte = aoc.Range(0, 0)

        r = ratings[category]
        if value in r:
            lte = aoc.Range(r.start, value + 1)
            gt = aoc.Range(value + 1, r.end)
        elif r.end < value:
            lte = r
        else:
            gt = r

        lte_rating = {c: r for c, r in ratings.items()}
        lte_rating[category] = lte
        gt_rating = {c: r for c, r in ratings.items()}
        gt_rating[category] = gt

        return gt_rating, lte_rating

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
        category = cond[:index]
        value = cond[index + 1 :]
        cond_expr = less_than(category, int(value))
        index = actions.index(",")
        true_action = parse_workflow(actions[:index])
        false_action = parse_workflow(actions[index + 1 :])
        return conditional_expr(cond_expr, true_action, false_action)

    elif ">" in cond:
        index = cond.index(">")
        category = cond[:index]
        value = cond[index + 1 :]
        index = actions.index(",")
        cond_expr = greater_than(category, int(value))
        true_action = parse_workflow(actions[:index])
        false_action = parse_workflow(actions[index + 1 :])
        return conditional_expr(cond_expr, true_action, false_action)
    else:
        raise ValueError(f"Invalid workflow: '{workflow}'")


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
            valid = True
            for category in "xmas":
                valid_range = valid_ranges[category]
                if rating[category] not in valid_range:
                    valid = False
                    break

            if valid:
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
