import aoc

tester = aoc.Tester("Scratchcards")


def parse(data: str) -> dict[int, dict[str, set[int]]]:
    cards = {}
    for line in data.splitlines():
        game, card_nums = line.split(":")
        game = int(game[4:])
        win, nums = card_nums.split("|")

        win_nums = set(map(int, win.strip().split()))
        scratch_nums = set(map(int, nums.strip().split()))

        cards[game] = {"win": win_nums, "scratch": scratch_nums}
    return cards


def calculate_winnings(cards: dict[int, dict[str, set[int]]]) -> int:
    winnings = 0
    for game, card in cards.items():
        win_count = len(card["win"].intersection(card["scratch"]))

        if win_count > 0:
            winnings += 2 ** (win_count - 1)
    return winnings


def calculate_real_winnings(cards: dict[int, dict[str, set[int]]]) -> int:
    card_count = {game: 1 for game in cards.keys()}
    scoring = {}
    for game, card in cards.items():
        scoring[game] = len(card["win"].intersection(card["scratch"]))

    winnings = {game: 1 for game in cards.keys()}
    while sum(winnings.values()):
        new_winnings = {game: 0 for game in cards.keys()}
        for game, win_count in winnings.items():
            score = scoring[game]
            for game_index in range(game + 1, game + score + 1):
                new_winnings[game_index] += win_count

        for game, win_count in new_winnings.items():
            card_count[game] += win_count
        winnings = new_winnings

    return sum(card_count.values())


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    data = aoc.read_input("input_test")
    cards = parse(data)

    t.test_value(calculate_winnings(cards), 13)

    t.test_value(calculate_real_winnings(cards), 30)


run_tests(tester)

data = aoc.read_input()
cards = parse(data)

tester.test_section("Part 1")
tester.test_solution(calculate_winnings(cards), 23441)

tester.test_section("Part 2")
tester.test_solution(calculate_real_winnings(cards), 5923918)
