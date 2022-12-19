import dataclasses
import functools

import aoc

tester = aoc.Tester("Not Enough Minerals")


@dataclasses.dataclass
class MineralCost:
    name: str
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


@dataclasses.dataclass
class Blueprint:
    ore_robot: MineralCost
    clay_robot: MineralCost
    obsidian_robot: MineralCost
    geode_robot: MineralCost


@dataclasses.dataclass(eq=True, unsafe_hash=True)
class Resources:
    ores: int = 0
    clays: int = 0
    obsidians: int = 0
    geodes: int = 0
    ore_robots: int = 1
    clay_robots: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0


def parse_input(filename: str):
    data = aoc.read_input(filename)
    blueprints = []
    for line in data.splitlines():
        line = line.split(" ")
        ore_robot = MineralCost(name="ore", ore=int(line[6]))
        clay_robot = MineralCost(name="clay", ore=int(line[12]))
        obsidian_robot = MineralCost(name="obsidian", ore=int(line[18]), clay=int(line[21]))
        geode_robot = MineralCost(name="geode", ore=int(line[27]), obsidian=int(line[30]))
        blueprints.append(Blueprint(ore_robot, clay_robot, obsidian_robot, geode_robot))
    return blueprints


def can_afford(resources: Resources, cost: MineralCost):
    return (
        cost.ore <= resources.ores
        and cost.clay <= resources.clays
        and cost.obsidian <= resources.obsidians
    )


def make_robot(resources: Resources, cost: MineralCost):
    resources.ores -= cost.ore
    resources.clays -= cost.clay
    resources.obsidians -= cost.obsidian

    match cost.name:
        case "geode":
            resources.geode_robots += 1
        case "obsidian":
            resources.obsidian_robots += 1
        case "clay":
            resources.clay_robots += 1
        case "ore":
            resources.ore_robots += 1


def gather_resources(res: Resources):
    res.ores += res.ore_robots
    res.clays += res.clay_robots
    res.obsidians += res.obsidian_robots
    res.geodes += res.geode_robots


class BlueprintQualityChecker:
    def __init__(self, blueprint: Blueprint, runtime: int = 24):
        self.blueprint = blueprint
        self.runtime = runtime

        ore_robot = blueprint.ore_robot
        clay_robot = blueprint.clay_robot
        obsidian_robot = blueprint.obsidian_robot
        geode_robot = blueprint.geode_robot
        self.max_ore = max(ore_robot.ore, clay_robot.ore, obsidian_robot.ore, geode_robot.ore)
        self.max_clay = max(ore_robot.clay, clay_robot.clay, obsidian_robot.clay, geode_robot.clay)
        self.max_obsidian = max(
            ore_robot.obsidian,
            clay_robot.obsidian,
            obsidian_robot.obsidian,
            geode_robot.obsidian,
        )

        self.max_geodes = 0
        self.memo = set()

    def upper_bound_geodes(self, resources: Resources, t: int) -> int:
        time_left = self.runtime - t
        return (
            resources.geodes
            + resources.geode_robots * time_left
            + ((time_left - 1) * time_left // 2)
        )

    def upper_bound_obsidian(self, resources: Resources, t: int) -> int:
        time_left = self.runtime - t
        return (
            resources.obsidians
            + resources.obsidian_robots * time_left
            + ((time_left - 1) * time_left // 2)
        )

    @functools.lru_cache
    def check_blueprint_quality(self, res: Resources, t: int = 0):
        if t == self.runtime:
            # print(resources)
            if res.geodes > self.max_geodes:
                self.max_geodes = res.geodes
                # print(f"Max Geodes = {self.max_geodes}")
            return res.geodes

        geode_upper_bound = self.upper_bound_geodes(res, t)
        if geode_upper_bound < self.max_geodes:
            return 0

        obsidian_upper_bound = self.upper_bound_obsidian(res, t)
        if res.geode_robots == 0 and obsidian_upper_bound < self.blueprint.geode_robot.obsidian:
            return 0

        state = (
            t,
            res.ore_robots,
            res.clay_robots,
            res.obsidian_robots,
            res.geode_robots,
            res.ores,
            res.clays,
            res.obsidians,
            res.geodes,
        )
        if state not in self.memo:
            self.memo.add(state)
        else:
            return 0

        can_build = []
        bp = self.blueprint
        if can_afford(res, bp.geode_robot):
            can_build.append(bp.geode_robot)

        else:
            if res.obsidian_robots < self.max_obsidian and can_afford(res, bp.obsidian_robot):
                can_build.append(bp.obsidian_robot)

            if res.clay_robots < self.max_clay and can_afford(res, bp.clay_robot):
                can_build.append(bp.clay_robot)

            if res.ore_robots < self.max_ore and can_afford(res, bp.ore_robot):
                can_build.append(bp.ore_robot)

            can_build.append(None)  # wait

        gather_resources(res)

        max_geodes = 0
        for robot in can_build:
            new_res = dataclasses.replace(res)
            if robot:
                make_robot(new_res, robot)

            geodes = self.check_blueprint_quality(new_res, t + 1)
            if geodes > max_geodes:
                max_geodes = geodes

        return max_geodes


def calculate_quality(blueprints):
    value = 0
    for index, blueprint in enumerate(blueprints, start=1):
        bqc = BlueprintQualityChecker(blueprint)
        quality = bqc.check_blueprint_quality(Resources())
        value += index * quality
    return value


def calculate_best_of_three(blueprints):
    value = 1
    for index, blueprint in enumerate(blueprints[:3]):
        bqc = BlueprintQualityChecker(blueprint, runtime=32)
        quality = bqc.check_blueprint_quality(Resources())
        value *= quality
    return value


def run_tests(t: aoc.Tester):
    t.test_section("Tests Part1")
    blueprints = parse_input("test_input")
    bqc = BlueprintQualityChecker(blueprints[0])
    t.test_value(bqc.check_blueprint_quality(Resources()), 9)
    bqc = BlueprintQualityChecker(blueprints[1])
    t.test_value(bqc.check_blueprint_quality(Resources()), 12)
    t.test_value(calculate_quality(blueprints), 33)

    t.test_section("Tests Part1 Edge Cases")
    blueprints = parse_input("test_input_extra")
    bqc = BlueprintQualityChecker(blueprints[0])
    t.test_value(bqc.check_blueprint_quality(Resources()), 9)
    bqc = BlueprintQualityChecker(blueprints[1])
    t.test_value(bqc.check_blueprint_quality(Resources()), 0)

    t.test_section("Tests Part2")
    blueprints = parse_input("test_input")
    bqc = BlueprintQualityChecker(blueprints[0], runtime=32)
    t.test_value(bqc.check_blueprint_quality(Resources()), 56)
    bqc = BlueprintQualityChecker(blueprints[1], runtime=32)
    t.test_value(bqc.check_blueprint_quality(Resources()), 62)


run_tests(tester)

data = aoc.read_input()

blueprints = parse_input("input")

tester.test_section("Part 1")
quality = calculate_quality(blueprints)
tester.test_greater_than(quality, 1999, "too low")
tester.test_greater_than(quality, 2121, "too low")
tester.test_less_than(quality, 2380, "too high")
tester.test_value_neq(quality, 2144)
tester.test_value(quality, 2160, "solution to part 1=%s")

tester.test_section("Part 2")
prod = calculate_best_of_three(blueprints)
tester.test_value(prod, 13340, "solution to part 2=%s")
