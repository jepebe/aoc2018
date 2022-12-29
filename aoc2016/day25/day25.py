import aoc

tester = aoc.Tester("Clock Signal")


def create_computer(lines: list[str]):
    computer = {
        "pointer": 0,
        "registers": {"a": 0, "b": 0, "c": 0, "d": 0},
        "program": [line.strip() for line in lines],
    }
    return computer


def run_program(program: str, reg_a: int = 0, signal_count_target: int = 10):
    computer = create_computer(program.splitlines())
    computer["registers"]["a"] = reg_a
    ticks = 0
    output = "0"
    signal_count = 0
    while computer["pointer"] < len(computer["program"]):
        pointer = computer["pointer"]
        instruction = computer["program"][pointer]

        cmd, *arg = instruction.split()

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

            case ["out", reg] if reg in "abcd":
                if output == str(computer["registers"][reg]):
                    output = "0" if output == "1" else "1"
                    signal_count += 1
                else:
                    return 0
                computer["pointer"] += 1

            case rest:
                assert False, f"Unhandled instruction {rest}"

        ticks += 1
        if signal_count == signal_count_target:
            break

    return signal_count


def find_input() -> int:
    signal_count_target = 8
    for i in range(1000):
        signal_count = run_program(aoc.read_input(), reg_a=i, signal_count_target=signal_count_target)
        if signal_count == signal_count_target:
            return i
    assert False, "did not find solution"


tester.test_section("Part 1")
tester.test_solution(find_input(), 182)
