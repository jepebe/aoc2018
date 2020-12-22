import intcode as ic

tester = ic.Tester('Crab Combat')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.read().splitlines(keepends=False)
    return lines


def parse(lines):
    decks = {}
    player = 0
    for line in lines:
        if line.startswith('Player'):
            player += 1
            decks[player] = []
        elif line.strip():
            decks[player].append(int(line))
    return decks


def play_crab_combat(decks):
    while decks[1] and decks[2]:
        p1 = decks[1].pop(0)
        p2 = decks[2].pop(0)
        if p1 > p2:
            decks[1].append(p1)
            decks[1].append(p2)
        else:
            decks[2].append(p2)
            decks[2].append(p1)

    player, winner = (1, decks[1]) if decks[1] else (2, decks[2])
    return player, sum(d * (len(winner) - i) for i, d in enumerate(winner))


def play_recursive_combat(decks, game=1, memo=None):
    seen = set()
    seen.add((tuple(decks[1]), tuple(decks[2])))
    while decks[1] and decks[2]:
        p1 = decks[1].pop(0)
        p2 = decks[2].pop(0)

        if p1 <= len(decks[1]) and p2 <= len(decks[2]):
            new_deck = {1: decks[1][0:p1], 2: decks[2][0:p2]}
            p = play_recursive_combat(new_deck, game + 1, memo)
            winner = p == 1
        else:
            winner = p1 > p2

        if winner:
            decks[1].append(p1)
            decks[1].append(p2)
        else:
            decks[2].append(p2)
            decks[2].append(p1)

        deck = (tuple(decks[1]), tuple(decks[2]))
        if deck in seen:
            return 1

        seen.add(deck)

    return 1 if decks[1] else 2


def play_recursive_crab_combat(decks):
    player = play_recursive_combat(decks, memo={})
    winner = decks[player]
    return player, sum(d * (len(winner) - i) for i, d in enumerate(winner))


lines = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".splitlines(keepends=False)

decks = parse(lines)
tester.test_value(play_crab_combat(decks), (2, 306))

decks = parse(read_file())
_, score = play_crab_combat(decks)
tester.test_value(score, 32033, 'solution to part 1=%s')

decks = parse(lines)
tester.test_value(play_recursive_crab_combat(decks), (2, 291))

decks = parse(read_file())
_, score = play_recursive_crab_combat(decks)
tester.test_value(score, 34901, 'solution to part 2=%s')
