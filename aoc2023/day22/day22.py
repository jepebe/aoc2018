import typing

import aoc

tester = aoc.Tester("Sand Slabs")


class Brick:
    def __init__(
        self, f: tuple[int, int, int], t: tuple[int, int, int], label: int = None
    ):
        self._from = f
        self._to = t
        self._label = label

    @property
    def on_floor(self) -> bool:
        return self._from[2] == 1 or self._to[2] == 1

    def __str__(self) -> str:
        return f"{self._from}~{self._to}"

    def __repr__(self) -> str:
        index = self._label + ord("A")
        return f"{chr(index)}({self._from}~{self._to})"

    def copy(self) -> typing.Self:
        return Brick(self._from, self._to)

    def __lt__(self, other: typing.Self):
        return self._from[2] < other._from[2]

    def drop(self, levels: int = 1):
        self._from = (self._from[0], self._from[1], self._from[2] - levels)
        self._to = (self._to[0], self._to[1], self._to[2] - levels)

    def lift(self, levels: int = 1):
        self._from = (self._from[0], self._from[1], self._from[2] + levels)
        self._to = (self._to[0], self._to[1], self._to[2] + levels)

    def __contains__(self, item: typing.Self) -> bool:
        x_overlap = self._to[0] >= item._from[0] and item._to[0] >= self._from[0]
        y_overlap = self._to[1] >= item._from[1] and item._to[1] >= self._from[1]
        z_overlap = self._to[2] >= item._from[2] and item._to[2] >= self._from[2]

        return x_overlap and y_overlap and z_overlap

    def __eq__(self, other: typing.Self) -> bool:
        return self._label == other._label

    def __hash__(self) -> int:
        return hash(self._label)

    def below(self, other: typing.Self) -> bool:
        return min(self._to[2], self._from[2]) <= max(other._from[2], other._to[2])

    def overlap_2d(self, other: typing.Self) -> bool:
        x_overlap = self._to[0] >= other._from[0] and other._to[0] >= self._from[0]
        y_overlap = self._to[1] >= other._from[1] and other._to[1] >= self._from[1]
        return x_overlap and y_overlap

    @property
    def min_z(self) -> int:
        return min(self._from[2], self._to[2])

    @property
    def max_z(self) -> int:
        return max(self._from[2], self._to[2])


def parse(data: str) -> list[Brick]:
    bricks: list[Brick] = []
    count = 0
    for line in data.splitlines():
        f, t = line.split("~")
        f = tuple(map(int, f.split(",")))
        t = tuple(map(int, t.split(",")))
        bricks.append(Brick(f, t, count))
        count += 1

    return bricks


def stabilize(bricks: list[Brick]) -> list[Brick]:
    # drop all bricks until they are stable
    stable = []
    in_air = []
    for brick in bricks:
        if brick.on_floor:
            stable.append(brick)
        else:
            in_air.append(brick)

    stable = sorted(stable)
    in_air = sorted(in_air)

    while in_air:
        brick = in_air.pop(0)

        # find all bricks that overlap in x,y direction with the current brick
        # these are the only bricks that can be hit by the current brick on its way down
        may_hit = []
        for other in stable:
            if brick.overlap_2d(other):
                may_hit.append(other)

        # find the maximum drop for the brick
        drop = 999
        brick_z = brick.min_z
        for hit in may_hit:
            max_z = hit.max_z
            if max_z < brick_z:
                if brick_z - max_z < drop:
                    drop = brick_z - max_z

        # drop the brick as far as we can
        if drop == 999:
            # the brick does not hit any other bricks on its way down
            # we can drop the brick to the floor
            brick.drop(brick_z - 1)
        else:
            # drop the brick as far as we can
            brick.drop(drop - 1)
        stable.append(brick)

    assert len(stable) == len(bricks)
    return stable


def check_stability(bricks: list[Brick]) -> tuple[int, int]:
    # find all bricks that are safe to remove and count how many bricks they disintegrate if removed

    supported_by, supports = find_supports_and_supported(bricks)
    safe_to_remove = find_safe_bricks(bricks, supported_by, supports)
    disintegration = count_disintegration_for_each_brick(bricks, supported_by, supports)

    # all bricks that are safe to remove should not disintegrate any bricks
    for brick, value in disintegration.items():
        if brick in safe_to_remove:
            assert value == 0

    return len(safe_to_remove), sum(disintegration.values())


def count_disintegration_for_each_brick(
    bricks: list[Brick],
    supported_by: dict[Brick, list[Brick]],
    supports: dict[Brick, list[Brick]],
) -> dict[Brick, int]:
    # count how many bricks each brick disintegrates if removed
    disintegration = {}
    for brick in bricks:
        disintegration[brick] = 0
        disintegrated = {brick}
        queue = []
        queue.extend(supports[brick])

        while queue:
            b = queue.pop(0)

            if b in disintegrated:
                continue

            disintegrates = True
            for support in supported_by[b]:
                if support not in disintegrated:
                    disintegrates = False
                    break

            if disintegrates:
                disintegration[brick] += 1
                disintegrated.add(b)
                queue.extend(supports[b])
    return disintegration


def find_supports_and_supported(
    bricks: list[Brick],
) -> tuple[dict[Brick, list[Brick]], dict[Brick, list[Brick]]]:
    # find all bricks that are supported by a brick and all bricks that support a brick
    supported_by = {}
    supports = {}
    for brick in bricks:
        supported_by[brick] = []
        supports[brick] = []

        # find all bricks that overlap in x,y direction with the current brick
        # these are the only bricks that can be hit by the current brick on its way down
        may_hit = []
        for other in bricks:
            if other != brick and brick.overlap_2d(other):
                may_hit.append(other)

        brick.drop()
        for other in may_hit:
            if brick in other:
                supported_by[brick].append(other)

        brick.lift(2)
        for other in may_hit:
            if brick in other:
                supports[brick].append(other)
        brick.drop()
    return supported_by, supports


def find_safe_bricks(
    bricks: list[Brick],
    supported_by: dict[Brick, list[Brick]],
    supports: dict[Brick, list[Brick]],
) -> set[Brick]:
    # find all bricks that are safe to remove
    safe_to_remove = set()
    for brick in bricks:
        if len(supports[brick]) == 0:
            safe_to_remove.add(brick)
        else:
            is_safe_to_remove = True
            for dependent in supports[brick]:
                if len(supported_by[dependent]) == 1:
                    is_safe_to_remove = False
            if is_safe_to_remove:
                safe_to_remove.add(brick)
    return safe_to_remove


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    boxes = parse(aoc.read_input("input_test"))
    boxes = stabilize(boxes)

    stability, max_disintegrate = check_stability(boxes)
    t.test_value(stability, 5)
    t.test_value(max_disintegrate, 7)


run_tests(tester)

data = aoc.read_input()

boxes = stabilize(parse(data))
tester.test(True, "", "Stabilized")  # for timing

tester.test_section("Part 1")
solution_1, solution_2 = check_stability(boxes)
tester.test_solution(solution_1, 424)

tester.test_section("Part 2")
tester.test_solution(solution_2, 55483)
