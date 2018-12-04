import sys
import dateutil.parser

lines = sys.stdin.readlines()


# (10, 50)
# (99, 3, 45)
# (10, 24, 240)
# (99, 45, 4455)

# (1237, 473)
# (2039, 16, 27)
# (1237, 32, 39584)
# (2039, 27, 55053)


def parse_events(lines):
    events = {}

    for line in lines:
        line = line.strip()
        date = dateutil.parser.parse(line[1:17])

        event = line[19:]
        events[date] = event
    return events


def fill(start, stop, duty):
    if start > stop:
        start = 0

    for x in range(start, stop):
        duty[x] += 1


def process_events(events):
    dates = sorted(events.keys())
    guard_id = -1
    duty = {}
    start = None
    stop = None
    for date in dates:
        event = events[date]

        if event.startswith('Guard'):
            # did not wake up within the hour
            if start is not None and stop is None:
                fill(start, 60, duty[guard_id])

            guard_id = int(event[7:].split()[0])
            start = None
            stop = None

            if guard_id not in duty:
                duty[guard_id] = [0] * 60

        elif event.startswith('falls'):
            start = date.minute

        else:
            stop = date.minute
            fill(start, stop, duty[guard_id])

    # did not wake up within the hour
    if start is not None and stop is None:
        fill(start, 60, duty[guard_id])

    return duty


def calc_stats(duty):
    stats = {}

    for guard in duty:
        stats[guard] = {'id': guard}

        gd = duty[guard]
        stats[guard]['sum_sleep'] = sum(gd)
        stats[guard]['max_sleep'] = max(gd)
        stats[guard]['max_sleep_index'] = gd.index(stats[guard]['max_sleep'])

    # print(guard, stats[guard], duty[guard])
    return stats


def find_dict_max(dct, key):
    max_id = 0
    max_value = 0
    for id, value in dct.items():
        if value[key] > max_value:
            max_id = id
            max_value = value[key]
    return dct[max_id]


events = parse_events(lines)
duty = process_events(events)
stats = calc_stats(duty)

strategy_1 = find_dict_max(stats, 'sum_sleep')
print(strategy_1, strategy_1['max_sleep_index'] * strategy_1['id'])

strategy_2 = find_dict_max(stats, 'max_sleep')
print(strategy_2, strategy_2['max_sleep_index'] * strategy_2['id'])
