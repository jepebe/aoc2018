import aoc
import aoc.ocr

tester = aoc.Tester("Cathode-Ray Tube")


def parse_program(data: str):
    program_listing = []
    for line in data.splitlines():
        match line.split(sep=" "):
            case (instruction,):
                program_listing.append((instruction, 0))
            case (instruction, operand):
                program_listing.append((instruction, int(operand)))
            case _:
                raise UserWarning(f"Unknown instruction '{line}'")

    return program_listing


def check_signal_accumulator(cpu: dict):
    if cpu["cycle"] == cpu["next_signal_collector_cycle"]:
        cpu["signal_accumulator"] += cpu["x"] * cpu["cycle"]
        cpu["next_signal_collector_cycle"] += 40


def draw_sprite(cpu: dict):
    if cpu["x"] - 1 <= cpu["crt_x"] <= cpu["x"] + 1:
        pixel = "#"
    else:
        pixel = " "

    cpu["crt"][(cpu["crt_x"], cpu["crt_y"])] = pixel
    cpu["crt_x"] += 1
    if cpu["crt_x"] == 40:
        cpu["crt_x"] = 0
        cpu["crt_y"] += 1


def tick(cpu: dict):
    cpu["cycle"] += 1
    draw_sprite(cpu)
    check_signal_accumulator(cpu)


def run_program(program_listing: list[tuple[str, int]]) -> tuple[int, str]:
    cpu = {
        "cycle": 0,
        "x": 1,
        "signal_accumulator": 0,
        "next_signal_collector_cycle": 20,
        "crt": {},
        "crt_x": 0,
        "crt_y": 0,
    }

    for instruction, operand in program_listing:
        match instruction:
            case "noop":
                tick(cpu)
            case "addx":
                tick(cpu)
                tick(cpu)
                cpu["x"] += operand

    # aoc.print_map(cpu["crt"])
    return cpu["signal_accumulator"], aoc.ocr.ocr(cpu["crt"])


tester.test_section("Tests")

program = parse_program(aoc.read_input("test_input_1"))
tester.test_value(run_program(program)[0], 13140)

program = parse_program(aoc.read_input())

tester.test_section("Part 1")
signal_strength, message = run_program(program)
tester.test_value(signal_strength, 14560, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(message, "EKRHEPUZ", "solution to part 2=%s")
