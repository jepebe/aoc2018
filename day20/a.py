import sys
from itertools import combinations, product

lines = sys.stdin.readlines()

dirs = {
    'N': ((0, -1), '-'),
    'E': ((1, 0), '|'),
    'W': ((-1, 0), '|'),
    'S': ((0, 1), '-')
}


class Token(object):
    def __init__(self, regex, start):
        self.regex = regex
        self.start = start
        self.chars = None
        self.children = []

    # def print(self, prefix=''):
    #     result = self.name()
    #
    #     print('%s%s' % (prefix, result))
    #
    #     if self.children:
    #         print('%s--%s' % (prefix, len(self.children)))
    #         for child in self.children:
    #             child.print(prefix + '  ')

    def name(self, default='@'):
        if self.chars is None:
            return 'BAD'
        if self.chars == 0:
            return default

        return regex[self.start:self.start + self.chars]

    def flatten(self):
        if self.children:
            result = []
            for child in self.children:
                for flat in child.flatten():
                    result.append(self.name() + flat)

            return result
        else:
            return [self.name(default='')]

    def is_group(self):
        return len(self.children) > 0

    def __str__(self):
        result = self.name()
        if self.is_group():
            result += ' group: [('
            result += ', '.join("%s" % c for c in self.children)
            result += ')]'
        return result


def print_map(topo):
    minx = min(x[0] for x in topo)
    miny = min(x[1] for x in topo)
    maxx = max(x[0] for x in topo)
    maxy = max(x[1] for x in topo)

    for y in range(miny, maxy + 1):
        row = []
        for x in range(minx, maxx + 1):
            if (x, y) in topo:
                row.append(topo[(x, y)])
            else:
                row.append(' ')
        print(''.join(row))


def parse_line(line):
    end = line.index('$')
    regex = line[1:end]
    test_target = None
    if line.index('=') > 0:
        test_target = int(line[end + 2:])
    return regex, test_target


def add_room(topo, pos):
    x, y = pos
    topo[(x, y)] = '.'
    for p in ((x - 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x + 1, y - 1)):
        if p in topo and topo[p] != '#':
            print('What?', p)
        else:
            topo[p] = '#'


def expand(topo, pos, regex):
    x, y = pos
    while index < len(regex):
        c = regex[index]
        if c in ('N', 'E', 'W', 'S'):
            (dx, dy), w = dirs[c]
            x, y = (x + dx, y + dy)
            topo[(x, y)] = w
            x, y = (x + dx, y + dy)
            add_room(topo, (x, y))
        elif c == '(':
            index = expand(topo, (x, y), regex[index + 1])
        elif c == '|':
            x, y = pos
        elif c == ')':
            break

    return index


def parse(regex, start):
    tokens = [Token(regex, start)]
    idx = start
    while idx < len(regex):
        c = regex[idx]
        if c in ('N', 'E', 'W', 'S'):
            if tokens[-1].chars is None:
                tokens[-1].chars = 0
            tokens[-1].chars += 1
            idx += 1
        elif c == '(':
            idx, children = parse(regex, idx + 1)
            tokens[-1].children.extend(children)
            tokens.append(Token(regex, idx))
        elif c == '|':
            tokens.append(Token(regex, idx + 1))
            idx += 1
        elif c == ')':
            if regex[idx - 1] == '|':
                tokens[-1].chars = 0
            idx += 1
            break

    tokens = [t for t in tokens if t.children or t.chars is not None]
    return idx, tokens


for line in lines:
    regex, test = parse_line(line)

    index, tokens = parse(regex, 0)
    print(''.join(str(t) for t in tokens))

    tokens = [t.flatten() for t in tokens]
    print(tokens)

    topo = {}
    add_room(topo, (0, 0))

    # expand(topo, (0, 0), regex)
    # print_map(topo)
