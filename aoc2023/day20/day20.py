import aoc

tester = aoc.Tester("Pulse Propagation")


def parse(data: str) -> dict[str, dict]:
    graph = {}
    for line in data.splitlines():
        name, dest = line.split(" -> ")
        if name.startswith("%") or name.startswith("&"):
            t = name[0]
            name = name[1:]
        else:
            t = ""

        dest = dest.split(", ")
        graph[name] = {"dest": dest, "type": t}
    return graph


def pulse(
    graph: dict[str, dict], mem: dict, track: list[str] = None, debug: bool = False
) -> tuple[int, int, list[str]]:
    low_pulses = 0
    high_pulses = 0
    queue = [("low", "broadcaster", "button")]
    tracked = []
    while queue:
        pulse, name, sender = queue.pop(0)

        if track and pulse == "high" and name in track:
            tracked.append(sender)

        if debug:
            print(f"{sender} -{pulse}-> {name}")

        match pulse:
            case "low":
                low_pulses += 1
            case "high":
                high_pulses += 1

        if name not in graph:
            # print(f"unknown node: {name}")
            mem[name] = {}
            t = "debug"
            dest = []
        else:
            t, dest = graph[name]["type"], graph[name]["dest"]

        match t:
            case "":
                for d in dest:
                    queue.append((pulse, d, name))
            case "%":
                if pulse == "low":
                    mem[name] = not mem[name]
                    if mem[name]:
                        pulse = "high"
                    else:
                        pulse = "low"

                    for d in dest:
                        queue.append((pulse, d, name))
            case "&":
                mem[name][sender] = pulse

                if all(p == "high" for p in mem[name].values()):
                    next_pulse = "low"
                else:
                    next_pulse = "high"

                for d in dest:
                    queue.append((next_pulse, d, name))
            case "debug":
                mem[name][sender] = pulse

    return low_pulses, high_pulses, tracked


def pulser(
    count: int, graph: dict[str, dict], rx_mode: bool = False, debug: bool = False
) -> int:
    low_pulses = 0
    high_pulses = 0

    mem = {}
    for n in graph.keys():
        match graph[n]["type"]:
            case "":
                mem[n] = 0
            case "%":
                mem[n] = 0
            case "&":
                mem[n] = {}

                for src, data in graph.items():
                    if n in data["dest"]:
                        mem[n][src] = "low"

    track = None
    if rx_mode:
        track = ["ll"]

    tracked_cycles = {}
    diff_cycles = {}

    counter = 0
    while counter < count or rx_mode:
        l, p, tracked = pulse(graph, mem, track=track, debug=debug)
        low_pulses += l
        high_pulses += p

        if rx_mode and tracked:
            for t in tracked:
                if t not in tracked_cycles:
                    tracked_cycles[t] = counter
                else:
                    diff = counter - tracked_cycles[t]
                    if t not in diff_cycles:
                        diff_cycles[t] = diff

            if len(diff_cycles) == len(tracked_cycles):
                # we found all cycles
                break

        counter += 1
    if rx_mode:
        lcm = aoc.lcms(*(int(v) for v in diff_cycles.values()))
        return lcm
    return low_pulses * high_pulses


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    graph = parse(aoc.read_input("input_test_1"))
    t.test_value(pulser(1000, graph), 32000000)

    graph = parse(aoc.read_input("input_test_2"))
    t.test_value(pulser(1000, graph, debug=False), 11687500)


run_tests(tester)

data = aoc.read_input()
graph = parse(data)

tester.test_section("Part 1")
solution_1 = pulser(1000, graph)
tester.test_solution(solution_1, 743090292)

tester.test_section("Part 2")
solution_2 = pulser(-1, graph, rx_mode=True)
tester.test_greater_than(solution_2, 49140182360)
tester.test_solution(solution_2, 0)
