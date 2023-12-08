import aoc

tester = aoc.Tester("Haunted Wasteland")


def parse(data: str) -> tuple[str, dict[str, tuple[str, str]]]:
    lines = data.splitlines()
    path = lines[0]
    nodes = {}

    for step in lines[2:]:
        node, neighbors = step.split(" = ")
        a, b = neighbors[1:9].split(", ")
        nodes[node] = (a, b)

    return path, nodes


def follow_map(path: str, nodes: dict[str, tuple[str, str]]) -> int:
    steps = 0
    node = "AAA"
    while node != "ZZZ":
        step = path[steps % len(path)]
        steps += 1
        if step == "R":
            node = nodes[node][1]
        elif step == "L":
            node = nodes[node][0]
        else:
            raise ValueError(f"Invalid step: {step}")
    return steps


def parallel_follow_map(path: str, nodes: dict[str, tuple[str, str]]) -> int:
    steps = 0
    current_nodes = [node for node in nodes if node.endswith("A")]
    repeat = {}
    while not all(node.endswith("Z") for node in current_nodes):
        next_nodes = []
        step = path[steps % len(path)]
        steps += 1
        for node in current_nodes:
            if step == "R":
                next_nodes.append(nodes[node][1])
            elif step == "L":
                next_nodes.append(nodes[node][0])
            else:
                raise ValueError(f"Invalid step: {step}")

        for index, node in enumerate(next_nodes):
            if node.endswith("Z") and index not in repeat:
                repeat[index] = steps
        current_nodes = next_nodes
        if len(repeat) == len(current_nodes):
            break

    return aoc.lcms(*repeat.values())  # least common multiple for all repeats


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test_1")
    path, nodes = parse(data)

    t.test_value(follow_map(path, nodes), 2)

    data = aoc.read_input("input_test_2")
    path, nodes = parse(data)

    t.test_value(follow_map(path, nodes), 6)

    data = aoc.read_input("input_test_3")
    path, nodes = parse(data)
    t.test_value(parallel_follow_map(path, nodes), 6)


run_tests(tester)

data = aoc.read_input()
path, nodes = parse(data)

tester.test_section("Part 1")
tester.test_solution(follow_map(path, nodes), 15989)

tester.test_section("Part 2")
tester.test_solution(parallel_follow_map(path, nodes), 13830919117339)
