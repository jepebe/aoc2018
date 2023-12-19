from pprint import pprint

import aoc

tester = aoc.Tester("Aplenty")

Rating = dict[str, set[aoc.Range]]
Workflows = dict[str, callable]


def accept_or_reject(workflow: str) -> callable:
    def f(workflows: Workflows, ratings: Rating, accepted: list) -> int:
        if workflow == "A":
            # print(" A ")
            combinations = 1
            for r_list in ratings.values():
                combinations *= sum(len(r) for r in r_list)
            print(f"accepted: {ratings} -> {combinations}")
            if combinations > 0:
                accepted.append(ratings)
            return combinations
        elif workflow == "R":
            print(f"rejected: {ratings}")
            # print(" R ")
            return 0
        else:
            raise ValueError(f"Invalid workflow: {workflow}")

    return f


def workflow_expr(workflow: str) -> callable:
    def f(workflows: Workflows, ratings: Rating, accepted: list) -> int:
        # print(f"{workflow} -> ", end="")
        return workflows[workflow](workflows, ratings, accepted)

    return f


def less_than(category: str, value: int) -> callable:
    def f(ratings: Rating) -> tuple[Rating, Rating]:
        # print(f"({category} < {value}) -> ", end="")
        ranges = ratings[category]
        gte = set()
        lt = set()
        for r in ranges:
            if value in r:
                lt.add(aoc.Range(r.start, value))
                gte.add(aoc.Range(value, r.end))
            elif r.end <= value:
                lt.add(r)
            else:
                gte.add(r)

        lt_rating = {c: r for c, r in ratings.items()}
        lt_rating[category] = lt
        gte_rating = {c: r for c, r in ratings.items()}
        gte_rating[category] = gte
        return lt_rating, gte_rating

    return f


def greater_than(category: str, value: int) -> callable:
    def f(ratings: Rating) -> tuple[Rating, Rating]:
        # print(f"({category} > {value}) -> ", end="")
        ranges = ratings[category]
        gt = set()
        lte = set()
        for r in ranges:
            if value in r:
                lte.add(aoc.Range(r.start, value + 1))
                gt.add(aoc.Range(value + 1, r.end))
            elif r.end < value:
                lte.add(r)
            else:
                gt.add(r)

        if len(gt) == 0:
            gt.add(aoc.Range(value + 1, 4001))
            # print(f"empty set: {category} > {value} -> {gt} {lte}")

        lte_rating = {c: r for c, r in ratings.items()}
        lte_rating[category] = lte
        gt_rating = {c: r for c, r in ratings.items()}
        gt_rating[category] = gt

        return lte_rating, gt_rating

    return f


def conditional_expr(conditional, true_action, false_action) -> callable:
    def f(workflows: Workflows, ratings: Rating, accepted: list) -> int:
        true_ratings, false_ratings = conditional(ratings)

        result = true_action(workflows, true_ratings, accepted)
        result += false_action(workflows, false_ratings, accepted)
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
        "x": {aoc.Range(1, 4001)},
        "m": {aoc.Range(1, 4001)},
        "a": {aoc.Range(1, 4001)},
        "s": {aoc.Range(1, 4001)},
    }
    accepted = []
    _ = workflows["in"](workflows, rating_ranges, accepted)

    valid_ratings = []
    for rating in ratings:
        print(f"rating: {rating}")
        for valid_ranges in accepted:
            valid = True
            for category in "xmas":
                valid_category = False
                for valid_range in valid_ranges[category]:
                    if rating[category] not in valid_range:
                        valid_category = True
                        break
                if not valid_category:
                    valid = False
                    break

            if valid:
                print(f"valid: {rating} in {valid_ranges}")
                valid_ratings.append(rating)
                break

    return sum(sum(rating.values()) for rating in valid_ratings)


def process_ranges(workflows: Workflows) -> int:
    ratings = {
        "x": {aoc.Range(1, 4001)},
        "m": {aoc.Range(1, 4001)},
        "a": {aoc.Range(1, 4001)},
        "s": {aoc.Range(1, 4001)},
    }
    accepted = []
    result = workflows["in"](workflows, ratings, accepted)

    for rating in accepted:
        for category in "xmas":
            for r in rating[category]:
                print(f"{category}: [{r.start:4d} - {r.end:4d}]", end=" ")
        print()
    return result


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
# solution_1 = process(*parse(data))
# tester.test_solution(solution_1, 575412)

tester.test_section("Part 2")
# solution_2 = process_ranges(workflows)
# tester.test_solution(solution_2, 208191)
