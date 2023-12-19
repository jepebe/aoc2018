import aoc

tester = aoc.Tester("Aplenty")


def parse_workflow(workflow: str) -> callable:
    def less_than(category: str, value: int):
        def f(ratings: dict[str, int]) -> bool:
            return ratings[category] < value
        return f

    def greater_than(category: str, value: int):
        def f(ratings: dict[str, int]) -> bool:
            return ratings[category] > value
        return f

    def conditional_expr(conditional, true_action, false_action):
        def f(ratings: dict[str, int]) -> bool:
            if conditional(ratings):
                return action(ratings)
            return False
        return f

    cond, actions = workflow.split(":")
    if "<" in cond:
        category, value = cond.split("<")



        return less_than(category, )

def parse(data: str) -> tuple[dict[str, str], list[dict[str, int]]]:
    rating_mode = False
    workflows = {}
    rating_list = []
    for line in data.splitlines():
        if line == "":
            rating_mode = True
            continue

        if not rating_mode:
            name = line[:line.index("{")]
            workflow = line[line.index("{") + 1:line.index("}")]
            workflows[name] = parse_workflow(workflow)
        else:
            rating = line[1:-1].split(",")
            ratings = {}
            for r in rating:
                r = r.split("=")
                ratings[r[0]] = int(r[1])

    print(workflows)
    return workflows, rating_list


def process(workflows: dict[str, str], ratings: list[dict[str, int]]) -> int:

    return 0

def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    workflows, ratings = parse(data)

    t.test_value(process(workflows, ratings), 19114)



run_tests(tester)

data = aoc.read_input()

tester.test_section("Part 1")
tester.test_solution(1, 71502)

tester.test_section("Part 2")
tester.test_solution(2, 208191)
