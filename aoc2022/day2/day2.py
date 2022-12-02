import aoc

tester = aoc.Tester("Rock Paper Scissors")

tester.test_section("Tests")

test_data = """A Y
B X
C Z"""


def parse_plays(data):
    return [(line[0], line[2]) for line in data.split("\n")]


game_map = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors",
}

scores = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3,
}


def outcome(opponent, player):
    if opponent == player:
        return 3

    if opponent == "Scissors" and player == "Rock":
        return 6

    if opponent == "Scissors" and player == "Paper":
        return 0

    if opponent == "Rock" and player == "Scissors":
        return 0

    if opponent == "Rock" and player == "Paper":
        return 6

    if opponent == "Paper" and player == "Scissors":
        return 6

    if opponent == "Paper" and player == "Rock":
        return 0


def play_strategy(result, opponent):
    if result == "X":  # lose
        if opponent == "Rock":
            player = "Scissors"
        elif opponent == "Paper":
            player = "Rock"
        else:
            player = "Paper"
    elif result == "Z":  # win
        if opponent == "Rock":
            player = "Paper"
        elif opponent == "Paper":
            player = "Scissors"
        else:
            player = "Rock"
    else:  # draw
        player = opponent
    return player


def score_game_a(plays):
    score = 0
    for a, b in plays:
        opponent = game_map[a]
        player = game_map[b]

        score += outcome(opponent, player)
        score += scores[player]

    return score


def score_game_b(plays):
    score = 0
    for a, b in plays:
        opponent = game_map[a]
        player = play_strategy(b, opponent)

        score += outcome(opponent, player)
        score += scores[player]

    return score


plays = parse_plays(test_data)

tester.test_value(score_game_a(plays), 15)
tester.test_value(score_game_b(plays), 12)

with open("input") as f:
    data = f.read()

plays = parse_plays(data)

tester.test_section("Part 1")
tester.test_value(score_game_a(plays), 11841, 'solution to part 1=%s')

tester.test_section("Part 2")
tester.test_value(score_game_b(plays), 13022, 'solution to part 2=%s')
