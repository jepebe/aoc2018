from collections import deque

goals = [(9, 25, 32),
         (10, 1618, 8317),
         (13, 7999, 146373),
         (17, 1104, 2764),
         (21, 6111, 54718),
         (30, 5807, 37305),
         (447, 71510, '?'),
         (447, 71510 * 100, '?')
         ]


def play_game(players, last_marble):
    scores = [0] * players

    marbles = deque([0])

    for marble in range(1, last_marble + 1):
        player = marble % players

        if marble % 23 == 0:
            marbles.rotate(7)
            scores[player] += marble + marbles.popleft()

        else:
            marbles.rotate(-2)
            marbles.appendleft(marble)

    return max(scores)


for goal in goals[0:]:
    players, last_marble, high_score = goal
    score = play_game(players, last_marble)

    print('score: %i == %s' % (score, high_score))
