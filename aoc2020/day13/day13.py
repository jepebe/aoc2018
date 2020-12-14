import intcode as ic

tester = ic.Tester('Shuttle Search')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def split_buses(bus_ids):
    buses = []

    i = 0
    for bus in bus_ids.split(','):
        if bus != 'x':
            buses.append((i, int(bus)))
        i += 1
    return buses


def find_bus(start, buses):
    i = start
    while True:
        for _, bus in buses:
            if i % bus == 0:
                return (i - start) * bus
        i += 1


def bus_departures(buses):
    sch = {bus: 0 for _, bus in buses}
    t = 0
    sync = {}
    max_delay, step = max((b for b in buses), key=lambda x: x[1])
    desc = list(reversed(sorted(buses, key=lambda x: x[1])))
    max_sync_count = 0
    while True:
        t += step
        count = 0
        for delay, bus in buses:
            sch[bus] = (t - max_delay + delay) % bus
            if sch[bus] == 0:
                count += 1

        sync_count = 0
        for b in desc:
            if sch[b[1]] == 0:
                sync_count += 1
            else:
                break

        if sync_count > 1:
            if sync_count not in sync:
                sync[sync_count] = t
            else:
                if sync_count > max_sync_count:
                    step = t - sync[sync_count]
                    max_sync_count = sync_count
                    print(t, sch, max_sync_count, step)

        if count == len(buses):
            break
    return t - max_delay


start, bus_ids = """939
7,13,x,x,59,x,31,19
""".splitlines()

tester.test_value(find_bus(int(start), split_buses(bus_ids)), 295)
tester.test_value(bus_departures(split_buses(bus_ids)), 1068781)
tester.test_value(bus_departures(split_buses('17,x,13,19')), 3417)
tester.test_value(bus_departures(split_buses('67,7,59,61')), 754018)
tester.test_value(bus_departures(split_buses('67,x,7,59,61')), 779210)
tester.test_value(bus_departures(split_buses('67,7,x,59,61')), 1261476)
tester.test_value(bus_departures(split_buses('1789,37,47,1889')), 1202161486)

start, bus_ids = read_file()
buses = split_buses(bus_ids)
tester.test_value(find_bus(int(start), buses), 207, 'solution to exercise 1=%s')
tester.test_value(bus_departures(buses), 530015546283687, 'solution to exercise 2=%s')
