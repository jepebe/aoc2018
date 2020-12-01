import intcode as ic

clues = [
    'children: 3',
    'cats: 7',
    'samoyeds: 2',
    'pomeranians: 3',
    'akitas: 0',
    'vizslas: 0',
    'goldfish: 5',
    'trees: 3',
    'cars: 2',
    'perfumes: 1',
]


def parse():
    with open('input') as f:
        lines = f.readlines()

    sue_clue = {}

    def add_attrib(attrib):
        if attrib not in sue_clue:
            sue_clue[attrib] = []
        sue_clue[attrib].append(sue)

    for line in lines:
        idx = line.find(':')
        sue = line[:idx]
        attributes = map(str.strip, line[idx + 1:].split(','))
        for attrib in attributes:
            add_attrib(attrib)
    return sue_clue


def find_matches(sue_clue, clues, add_range=False):
    match_list = {}

    def match_clue(clue):
        if clue in sue_clue:
            match_list[clue] = sue_clue[clue]

    for clue in clues:
        startswith = clue.startswith  # prettyfication
        if add_range and (startswith('cats') or startswith('trees')):
            idx = clue.find(':')
            count = int(clue[idx + 1:].strip())
            for i in range(count + 1, 11):
                match_clue(f'{clue[:idx + 2]}{i}')
        elif add_range and (startswith('pomeranians') or startswith('goldfish')):
            idx = clue.find(':')
            count = int(clue[idx + 1:].strip())
            for i in range(count - 1, -1, -1):
                match_clue(f'{clue[:idx + 2]}{i}')
        else:
            match_clue(clue)

    return match_list


def find_max_sue(match_list):
    count = {}
    for attrib, sues in match_list.items():
        for sue in sues:
            if sue not in count:
                count[sue] = 0
            count[sue] += 1

    return max(count, key=count.get)


sue_clue = parse()
match_list = find_matches(sue_clue, clues)
max_sue = find_max_sue(match_list)

tester = ic.Tester('Aunt Sue')
tester.test_value(max_sue, 'Sue 40', 'solution to exercise 1 = %s')

sue_clue = parse()
match_list = find_matches(sue_clue, clues, add_range=True)
max_sue = find_max_sue(match_list)

tester.test_value(max_sue, 'Sue 241', 'solution to exercise 2 = %s')
