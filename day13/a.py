import sys

lines = sys.stdin.readlines()

directions = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1),
}

turns = ['left', 'straight', 'right']
turning = {
    '>': {'left': '^', 'straight': '>', 'right': 'v'},
    '<': {'left': 'v', 'straight': '<', 'right': '^'},
    '^': {'left': '<', 'straight': '^', 'right': '>'},
    'v': {'left': '>', 'straight': 'v', 'right': '<'},
}


def parse_map(lines):
    topology = {}
    carts = []

    x = 0
    y = 0
    for line in lines:
        for c in line:
            if c == '<' or c == '>':
                topology[(x, y)] = '-'
                carts.append({'pos': (x, y), 'dir': c, 'turn': 0})
            elif c == '^' or c == 'v':
                topology[(x, y)] = '|'
                carts.append({'pos': (x, y), 'dir': c, 'turn': 0})
            elif c in ['-', '|', '/', '+', '\\']:
                topology[(x, y)] = c
            else:
                if c not in [' ', '\n']:
                    print('Unknown', c)

            x += 1
        x = 0
        y += 1

    return topology, carts


topology, carts = parse_map(lines)


# print(topology)
# print(carts)

def cart_sorter(x):
    p = x['pos']
    return p[1], p[0]


def tick(topology, carts):
    crash_list = []
    for cart in sorted(carts, key=cart_sorter):

        if cart in crash_list:
            continue

        pos = cart['pos']
        direction = cart['dir']
        vector = directions[direction]

        new_pos = pos[0] + vector[0], pos[1] + vector[1]

        if new_pos in topology:
            if topology[new_pos] == '/':
                if vector[0] == 1:
                    new_dir = '^'
                elif vector[0] == -1:
                    new_dir = 'v'
                elif vector[1] == -1:
                    new_dir = '>'
                elif vector[1] == 1:
                    new_dir = '<'
            elif topology[new_pos] == '\\':
                if vector[0] == 1:
                    new_dir = 'v'
                elif vector[0] == -1:
                    new_dir = '^'
                elif vector[1] == -1:
                    new_dir = '<'
                elif vector[1] == 1:
                    new_dir = '>'
            elif topology[new_pos] == '+':
                turn_direction = turns[cart['turn']]
                turn = turning[direction][turn_direction]
                new_dir = turn
                cart['turn'] += 1
                if cart['turn'] == 3:
                    cart['turn'] = 0

            elif topology[new_pos] in ['-', '|']:
                new_dir = direction
            else:
                print('What?', topology[new_pos], topology[pos])

            cart['pos'] = new_pos
            cart['dir'] = new_dir

        else:
            print('Whaattt??', new_pos)

        positions = {c['pos']: c for c in carts if c != cart and c not in crash_list}
        if new_pos in positions:
            crash_list.append(cart)
            crash_list.append(positions[new_pos])

    return crash_list


def print_topology(topology, carts):
    for y in range(7):
        row = []
        for x in range(15):
            if (x, y) in carts:
                row.append(carts[(x, y)]['dir'])
            elif (x, y) in topology:
                row.append(topology[(x, y)])
            else:
                row.append(' ')

        print(''.join(row))


# print_topology(topology, {x['pos']: x for x in carts})

i = 0
while i < 20000:
    old_positions = {c['pos']: c for c in carts}
    crash_list = tick(topology, carts)

    if len(crash_list) > 0:
        print('tick crash', crash_list)

    carts = [cart for cart in carts if cart not in crash_list]
    # print_topology(topology, {x['pos']: x for x in carts})
    if len(carts) == 1:
        # print_topology(topology, {x['pos']: x for x in carts})
        print(i, carts[0]['pos'])
        break
    i += 1
