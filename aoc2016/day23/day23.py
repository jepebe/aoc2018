import aoc

tester = aoc.Tester("Safe Cracking")


def create_computer(lines: list[str]):
    computer = {
        "pointer": 0,
        "registers": {"a": 0, "b": 0, "c": 0, "d": 0},
        "program": [line.strip() for line in lines],
    }
    return computer


def run_program(program: str, reg_a: int = 0):
    computer = create_computer(program.splitlines())
    computer["registers"]["a"] = reg_a
    ticks = 0
    toggle = {index: False for index in range(len(computer["program"]))}
    while computer["pointer"] < len(computer["program"]):
        pointer = computer["pointer"]
        instruction = computer["program"][pointer]

        cmd, *arg = instruction.split()
        orig_cmd = cmd
        if toggle[pointer]:
            match cmd:
                case "inc":
                    cmd = "dec"
                case "dec" | "tgl":
                    cmd = "inc"
                case "jnz":
                    cmd = "cpy"
                case "cpy":
                    cmd = "jnz"
                case _:
                    assert False, f"Unhandled op {cmd}"

        # print(f"{pointer + 1:2}, {orig_cmd} {cmd} {str(arg):<15}", end=" ")
        # r = computer["registers"]
        # print(f"a={r['a']:<7} b={r['b']:<7} c={r['c']:<7} d={r['d']:<7}")

        match cmd, *arg:
            case ["cpy", src, dst] if src in "abcd" and dst in "abcd":
                computer["registers"][dst] = computer["registers"][src]
                computer["pointer"] += 1

            case ["cpy", value, reg] if reg in "abcd":
                computer["registers"][reg] = int(value)
                computer["pointer"] += 1

            case ["inc", reg] if reg in "abcd":
                computer["registers"][reg] += 1
                computer["pointer"] += 1

            case ["mul", a, b, dst] if a in "abcd" and b in "abcd" and dst in "abcd":
                computer["registers"][dst] = computer["registers"][a] * computer["registers"][b]
                computer["pointer"] += 1

            case ["dec", reg] if reg in "abcd":
                computer["registers"][reg] -= 1
                computer["pointer"] += 1

            case ["jnz", reg, jmp] if reg in "abcd":
                if computer["registers"][reg] != 0:
                    computer["pointer"] += int(jmp)
                else:
                    computer["pointer"] += 1

            case ["jnz", value, jmp_reg] if jmp_reg in "abcd":
                if int(value) != 0:
                    computer["pointer"] += computer["registers"][jmp_reg]
                else:
                    computer["pointer"] += 1

            case ["jnz", value, jmp]:
                if int(value) != 0:
                    computer["pointer"] += int(jmp)
                else:
                    computer["pointer"] += 1

            case ["tgl", reg]:
                value = pointer + computer["registers"][reg]
                if value in toggle:
                    toggle[value] = not toggle[value]
                computer["pointer"] += 1

            case rest:
                assert False, f"Unhandled instruction {rest}"

        ticks += 1

    # print(f"{ticks=}")
    return computer["registers"]["a"]


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    prg = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""
    run_program(prg)


run_tests(tester)

tester.test_section("Part 1")
tester.test_solution(run_program(aoc.read_input(), reg_a=7), 12624)

tester.test_section("Part 2")
tester.test_solution(run_program(aoc.read_input(), reg_a=12), 479009184)
