import aoc

tester = aoc.Tester("Beacon Exclusion Zone")


def distance(t1, t2):
    return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])


def parse_input(filename: str):
    data = aoc.read_input(filename)
    sensors_and_beacons = {}
    for line in data.splitlines():
        _, _, sensor_x, sensor_y, _, _, _, _, beacon_x, beacon_y = line.split(" ")
        sensor = int(sensor_x[2:-1]), int(sensor_y[2:-1])
        beacon = int(beacon_x[2:-1]), int(beacon_y[2:])
        sensors_and_beacons[sensor] = beacon

    return sensors_and_beacons


def follow_rim(pos: tuple[int, int], radius: int):
    rim = pos[0], pos[1] - radius - 1
    for direction in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
        for i in range(radius + 1):
            yield rim
            rim = aoc.add_tuple(rim, direction)


def count_where_beacon_is_not_at_row(s_and_b: dict[tuple, tuple], row: int):
    ext = aoc.find_extents(s_and_b)
    overlap_min = ext[1]  # max x
    overlap_max = ext[0]  # min x
    exclude = set()
    for sensor, beacon in s_and_b.items():
        if beacon[1] == row:
            exclude.add(beacon)

        sb_dist = distance(sensor, beacon)
        row_pos = (sensor[0], row)
        sr_dist = distance(sensor, row_pos)

        if sr_dist <= sb_dist:
            row_min_x = sensor[0] - (sb_dist - sr_dist)
            row_max_x = sensor[0] + (sb_dist - sr_dist)

            if row_min_x < overlap_min:
                overlap_min = row_min_x

            if row_max_x > overlap_max:
                overlap_max = row_max_x

    return (overlap_max - overlap_min + 1) - len(exclude)


def find_beacon_position(s_and_b: dict[tuple, tuple], search_space: int):
    sensor_dist = {s: distance(s, b) for s, b in s_and_b.items()}

    for sensor in s_and_b.keys():
        dist = sensor_dist[sensor]
        for rim in follow_rim(sensor, dist):
            if 0 <= rim[0] <= search_space and 0 <= rim[1] <= search_space:
                candidate = True
                for sens, dist in sensor_dist.items():
                    if distance(sens, rim) <= dist:
                        candidate = False
                        break

                if candidate:
                    return rim[0] * 4000000 + rim[1]
    raise UserWarning("No solution found! ¯\\_(ツ)_/¯")


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    rimmer = follow_rim((3, 5), 3)
    t.test_value(next(rimmer), (3, 1))
    t.test_value(next(rimmer), (4, 2))
    t.test_value(next(rimmer), (5, 3))
    t.test_value(next(rimmer), (6, 4))
    t.test_value(next(rimmer), (7, 5))
    t.test_value(next(rimmer), (6, 6))

    s_and_b = parse_input("test_input")
    tester.test_value(count_where_beacon_is_not_at_row(s_and_b, 10), 26)
    tester.test_value(find_beacon_position(s_and_b, 20), 56000011)


run_tests(tester)

sab = parse_input("input")

tester.test_section("Part 1")
tester.test_value(count_where_beacon_is_not_at_row(sab, 2000000), 5166077, "solution to part 1=%s")

tester.test_section("Part 2")
tester.test_value(find_beacon_position(sab, 4000000), 13_071_206_703_981, "solution to part 2=%s")
