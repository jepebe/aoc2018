import aoc

tester = aoc.Tester("Supply Stacks")

test_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

tester.test_section("Tests")


def parse_input(data: str) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    stacks = [""] * 10
    ops = []
    header = True
    for line in data.splitlines():
        if len(line) > 1 and line[1].isnumeric():
            header = False
            continue

        if line == "":
            continue

        if header:
            stack_index = 0
            for index, c in enumerate(line):
                if index > 0 and (index - 1) % 4 == 0:
                    if c.isalpha():
                        stacks[stack_index] = c + stacks[stack_index]
                    stack_index += 1

        else:
            _, count, _, from_stack, _, to_stack = line.split(sep=" ")
            ops.append((int(count), int(from_stack), int(to_stack)))
    stacks = [[c for c in stack] for stack in stacks if len(stack) > 0]
    return stacks, ops


def rearrange(stacks: list[list[str]], ops: list[tuple[int, int, int]]) -> str:
    for count, from_stack, to_stack in ops:
        for i in range(count):
            top = stacks[from_stack - 1].pop()
            stacks[to_stack - 1].append(top)

    result = []
    for stack in stacks:
        result.append(stack[-1])
    return "".join(result)


def rearrange_9001(stacks: list[list[str]], ops: list[tuple[int, int, int]]) -> str:
    for count, from_stack, to_stack in ops:
        top = stacks[from_stack - 1][-count:]
        for i in range(count):
            stacks[from_stack - 1].pop()
        stacks[to_stack - 1].extend(top)

    result = []
    for stack in stacks:
        result.append(stack[-1])
    return "".join(result)


expected_stacks = [["Z", "N"], ["M", "C", "D"], ["P"]]
expected_ops = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

test_stack, test_ops = parse_input(test_data)
tester.test_value(test_stack, expected_stacks)
tester.test_value(test_ops, expected_ops)

tester.test_value(rearrange(test_stack, test_ops), "CMZ")

test_stack, test_ops = parse_input(test_data)
tester.test_value(rearrange_9001(test_stack, test_ops), "MCD")

tester.test_section("Part 1")
stacks, ops = parse_input(aoc.read_input())
tester.test_value(rearrange(stacks, ops), "ZBDRNPMVH", "solution to part 1=%s")

tester.test_section("Part 2")
stacks, ops = parse_input(aoc.read_input())
tester.test_value(rearrange_9001(stacks, ops), "WDLPFNNNB", "solution to part 2=%s")
