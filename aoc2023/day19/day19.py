import aoc

tester = aoc.Tester("Aplenty")


def accept_or_reject(workflow: str) -> bool:
    def f(workflows: dict[str, callable], ratings: dict[str, int]) -> bool:
        if workflow == "A":
            # print(" A ")
            return True
        elif workflow == "R":
            # print(" R ")
            return False
        else:
            raise ValueError(f"Invalid workflow: {workflow}")

    return f


def workflow_expr(workflow: str):
    def f(workflows: dict[str, callable], ratings: dict[str, int]) -> bool:
        # print(f"{workflow} -> ", end="")
        return workflows[workflow](workflows, ratings)

    return f


def less_than(category: str, value: int):
    def f(ratings: dict[str, int]) -> bool:
        # print(f"({category} < {value}) -> ", end="")
        return ratings[category] < value

    return f


def greater_than(category: str, value: int):
    def f(ratings: dict[str, int]) -> bool:
        # print(f"({category} > {value}) -> ", end="")
        return ratings[category] > value

    return f


def conditional_expr(conditional, true_action, false_action):
    def f(workflows: dict[str, callable], ratings: dict[str, int]) -> bool:
        if conditional(ratings):
            return true_action(workflows, ratings)
        else:
            return false_action(workflows, ratings)

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


def parse(data: str) -> tuple[dict[str, callable], list[dict[str, int]]]:
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


def process(workflows: dict[str, callable], ratings: list[dict[str, int]]) -> int:
    accepted = []
    for rating in ratings:
        # print(rating)
        # print(f"in -> ", end="")
        workflow = workflows["in"]
        if workflow(workflows, rating):
            accepted.append(rating)
            continue

    return sum(sum(rating.values()) for rating in accepted)


def process_ranges(workflows: dict[str, callable]) -> int:
    ratings = {
        "x": aoc.Range(1, 4000),
        "m": aoc.Range(1, 4000),
        "a": aoc.Range(1, 4000),
        "s": aoc.Range(1, 4000),
    }

    workflow = workflows["in"]
    workflow(workflows, ratings)


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    workflows, ratings = parse(data)

    t.test_value(process(workflows, ratings), 19114)

    t.test_value(process_ranges(workflows), 167409079868000)


run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
solution_1 = process(*parse(data))
tester.test_solution(solution_1, 575412)

tester.test_section("Part 2")
tester.test_solution(2, 208191)
