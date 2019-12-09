import sys

lines = sys.stdin.readlines()
lines = [line.split(',') for line in lines]

DIRS = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def follow_wire(wires, wire, id):
    pos = (0, 0)
    signal = 0

    for d in wire:
        direction = DIRS[d[0]]
        steps = int(d[1:])

        for i in range(steps):
            pos = pos[0] + direction[0], pos[1] + direction[1]
            signal += 1
            if pos not in wires:
                wires[pos] = {'ids': {id},
                              'signal': {id: signal}}
            else:
                if id in wires[pos]['ids']:
                    intersection_signal = wires[pos]['signal'][id]
                else:
                    intersection_signal = signal

                wires[pos]['ids'].add(id)
                wires[pos]['signal'][id] = intersection_signal


def find_intersections(wires):
    intersections = []
    for pos, value in wires.items():
        if len(value['ids']) > 1:
            intersections.append((pos, value['signal']))
    return intersections


def find_min_distance(jumble):
    wires = {}

    follow_wire(wires, jumble[0], 'a')
    follow_wire(wires, jumble[1], 'b')

    intersections = find_intersections(wires)
    distances = [abs(x) + abs(y) for (x, y), _ in intersections]
    signals = [signal['a'] + signal['b'] for (_, _), signal in intersections]
    print(min(distances), min(signals))
    return min(distances), min(signals)


jumble = [['R8', 'U5', 'L5', 'D3'], ['U7', 'R6', 'D4', 'L4']]
assert find_min_distance(jumble) == (6, 30)

jumble = [['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
          ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']]
assert find_min_distance(jumble) == (159, 610)

jumble = [['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
          ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7']]
assert find_min_distance(jumble) == (135, 410)

assert find_min_distance(lines) == (1017, 11432)

