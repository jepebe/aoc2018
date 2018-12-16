import sys

from collections import deque

lines = sys.stdin.readlines()

test_data = []
lineno = 0
while not lines[lineno].startswith('#'):
    attack, turn, hp = map(int, lines[lineno].strip().split(','))
    test_data.append((attack, turn, hp))
    lineno += 1

lines = lines[lineno:]


class Unit(object):
    def __init__(self, mark, pos):
        self.mark = mark
        self.pos = pos
        self.attack = 3
        self.hp = 200

        self._pos = pos

    def reset(self, attack=3):
        self.pos = self._pos

        if self.mark == 'E':
            self.attack = attack
        self.hp = 200

    @property
    def alive(self):
        return self.hp > 0

    def __lt__(self, other):
        p = self.pos
        op = other.pos

        if op[1] == p[1]:
            return p[0] < op[0]
        return p[1] < op[1]

    def __repr__(self):
        state = 'alive' if self.alive else 'dead'
        return '%s [%s] A:%d HP:%d/200 @ (%s)' % (self.mark, state, self.attack, self.hp, self.pos)


def parse_input(lines):
    topo = {}
    eag = {}
    y = 0
    max_x = 0
    for line in lines:
        x = 0
        for c in line.strip():
            if c in ('#', '.'):
                topo[(x, y)] = c
            elif c in ('E', 'G'):
                eag[(x, y)] = Unit(c, (x, y))
                topo[(x, y)] = '.'
            else:
                print('Whatt?', c)
            x += 1

            if x > max_x:
                max_x = x

        y += 1

    return topo, eag, max_x, y


def print_map(topo, eag, max_x, max_y):
    for y in range(max_y):
        row = []
        units = []
        for x in range(max_x):
            if (x, y) in eag:
                unit = eag[(x, y)]
                row.append(unit.mark)
                units.append(' ')
                units.append(str(unit))
            else:
                row.append(topo[(x, y)])

        print(''.join(row + units))


def free(topo, eag, pos):
    return topo[pos] != '#' and pos not in [u.pos for u in eag.values() if u.alive]


def enemy_adjacent(eag, unit):
    x, y = unit.pos
    enemies = [u.pos for u in find_enemies(eag, unit)]

    adjacent_enemies = []
    for ap in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
        if ap in enemies:
            adjacent_enemies.append(eag[ap])
    return adjacent_enemies


def bfs(topo, eag, start, goal):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == goal:
            return path

        for pos in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if topo[pos] == '#':
                continue
            if pos in eag and eag[pos].alive:
                continue
            if pos in seen:
                continue

            queue.append(path + [pos])
            seen.add(pos)
    return False


def find_enemies(eag, unit):
    return sorted([u for u in eag.values() if u.mark != unit.mark and u.alive])


def find_paths(topo, eag, unit):
    paths = []
    for enemy in find_enemies(eag, unit):
        x, y = enemy.pos

        path = False
        for ap in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if free(topo, eag, ap):
                pth = bfs(topo, eag, unit.pos, ap)
                if pth and (not path or (len(pth) < len(path))):
                    path = pth

        if path:
            path = {
                'len': len(path),
                'enemy': enemy,
                'path': path[1:]
            }
            paths.append(path)

        paths = sorted(paths, key=lambda x: (x['len'], x['enemy']))

    return paths


def step_units(topo, eag):
    battle_over = False
    for unit in sorted(eag.values()):
        if unit.alive:
            enemies = find_enemies(eag, unit)
            if len(enemies) == 0:
                battle_over = True

            enemies = enemy_adjacent(eag, unit)
            if len(enemies) == 0:
                paths = find_paths(topo, eag, unit)
                del eag[unit.pos]
                if len(paths) > 0:
                    path = paths[0]
                    unit.pos = path['path'][0]

                eag[unit.pos] = unit

            enemies = enemy_adjacent(eag, unit)
            if len(enemies) > 0:
                enemy = sorted(enemies, key=lambda x: (x.hp, x))[0]
                enemy.hp -= unit.attack

    return battle_over


def unit_count(eag, mark):
    return sum(1 for x in eag.values() if x.mark == mark and x.alive)


def run_battle(topo, eag, attack):
    elves_count = unit_count(eag, 'E')

    turn = -1
    battle_over = False
    while not battle_over:
        turn += 1
        battle_over = step_units(topo, eag)

    score = 0
    for unit in [u for u in eag.values() if u.alive]:
        score += unit.hp if unit.hp > 0 else 0

    fight_score = (score * turn, turn, turn, score, attack)
    if unit_count(eag, 'E') != elves_count:
        print('Elves lost! Outcome %d after %d turns (%d * %d) [%d]' % fight_score)
    else:
        print('Elves won! Outcome %d after %d turns (%d * %d) [%d]' % fight_score)

    return unit_count(eag, 'E') == elves_count, turn, score


topo, eag, max_x, max_y = parse_input(lines)

attack = 2
elves_won = False
while not elves_won:
    attack += 1
    for unit in eag.values():
        unit.reset(attack)

    battle_units = {x.pos: x for x in eag.values()}

    elves_won, turn, score = run_battle(topo, battle_units, attack)

    for test_attack, test_turn, test_score in test_data:
        if attack == test_attack:
            if test_turn != turn or test_score != score:
                print('\033[31mFailed! (%d,%d) != (%d,%d)\033[0m' % (turn, score, test_turn, test_score))
            else:
                print('\033[92mSuccess! (%d,%d) == (%d,%d)\033[0m' % (turn, score, test_turn, test_score))

print('Attack level of %d needed for an outcome of %d' % (attack, turn*score))

# test2 -> 47 * 590 = 27730 -> 29 * 172 = 4988 (15)
# test3 -> 37 * 982 = 36334 ->
# test4 -> 46 * 859 = 39514 -> 33 * 948 = 31284 (4)
# test5 -> 35 * 793 = 27755 -> 37 * 94 = 3478 (15)
# test6 -> 54 * 536 = 28944 -> 39 * 166 = 6474 (12)
# test7 -> 20 * 937 = 18740 -> 30 * 38 = 1140 (34)

# 1: 84 206892 2463
# 2: 79 205795 2605
# 3: 82 212134 2587
# 4: 82 201638 2459 <-

# 1: 92 97336 1058
# 2: 92 97060 1055 = off-by-3-test
# 3: 89 95230 1070
# 4: 89 94963 1067 = off-by-3-test
# 5: 89 95764 1076 <- !!!
