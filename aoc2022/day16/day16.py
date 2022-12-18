import aoc

tester = aoc.Tester("Proboscidea Volcanium")


def parse_input(filename: str) -> dict[str, dict]:
    data = aoc.read_input(filename)
    valves = {}
    for line in data.splitlines():
        values = line.split(" ")
        valve_name = values[1]
        valve_rate = int(values[4].split("=")[1].replace(";", ""))
        neighbors = values[8:]

        valves[valve_name] = {
            "name": valve_name,
            "rate": valve_rate,
            "neighbors": [n.replace(",", "") for n in neighbors[1:]]
        }

    return valves


class Tunnels:
    def __init__(self, valves: dict[str, dict], dist: aoc.Distances):
        self.valves = valves
        self.dist = dist
        self.valves_with_flow = set([v for v in valves.keys() if valves[v]["rate"] > 0])
        self.max_pressure = 0

    def pressure(self, open_valves: set) -> int:
        p = 0
        for v in open_valves:
            p += self.valves[v]["rate"]
        return p

    def open_valve(self, current_valve: str, open_valves: set, t: int = 1, pressure: int = 0) -> int:
        current_pressure = self.pressure(open_valves)
        pressure += current_pressure

        if t == 30:
            return pressure

        if t > 30:
            return 0

        if current_valve in self.valves_with_flow and current_valve not in open_valves:
            open_valves = open_valves.union({current_valve})
            return self.open_valve(current_valve, open_valves, t + 1, pressure)

        if open_valves == self.valves_with_flow:
            jump = 30 - t - 1
            return self.open_valve(current_valve, open_valves, 30, pressure + current_pressure * jump)

        max_pressure = 0
        unopened_valves = [v for v in self.valves_with_flow if v not in open_valves]
        for v in unopened_valves:
            # distance to next operable valve
            dist = self.dist[(current_valve, v)]

            # winning solution may not have all valves open - duh!
            if t + dist > 30:
                dist = 30 - t

            # pressure released while moving to next valve
            new_pressure = pressure + current_pressure * (dist - 1)

            p = self.open_valve(v, open_valves, t + dist, new_pressure)

            if p > max_pressure:
                max_pressure = p

        return max_pressure

    def open_elephant_valve(self, valve: str, pressure: int, depth: int, open_valves: set, elephant: bool):
        if pressure >= self.max_pressure:
            self.max_pressure = pressure

        if depth <= 2:
            # I believe this works because if the valve has not been opened by now it will not
            # contribute anything on the next depth? Or not. Maybe just luck...
            return

        if valve in self.valves_with_flow and valve not in open_valves:
            new_open_valves = open_valves.union({valve})
            p = self.valves[valve]["rate"] * depth

            self.open_elephant_valve(valve, pressure + p, depth - 1, new_open_valves, elephant)
            if not elephant:
                self.open_elephant_valve("AA", pressure + p, 25, new_open_valves, True)

        else:
            for next_valve in [v for v in self.valves_with_flow if v not in open_valves]:
                dist = self.dist[(valve, next_valve)]
                self.open_elephant_valve(next_valve, pressure, depth - dist, open_valves, elephant)


def find_maximum_rate(filename: str) -> int:
    valves = parse_input(filename)
    distances = aoc.floyd_warshall(valves)
    t = Tunnels(valves, distances)
    return t.open_valve("AA", set())


def find_elephant_maximum_rate(filename: str) -> int:
    valves = parse_input(filename)
    distances = aoc.floyd_warshall(valves)
    t = Tunnels(valves, distances)
    t.open_elephant_valve("AA", pressure=0, depth=25, open_valves=set(), elephant=False)
    return t.max_pressure


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    t.test_value(find_maximum_rate("test_input"), 1651)
    t.test_value(find_elephant_maximum_rate("test_input"), 1707)


run_tests(tester)

tester.test_section("Part 1")
tester.test_value(find_maximum_rate("input"), 1474, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_elephant_maximum_rate("input"), 2100, "solution to part 2=%s")
