import sys

lines = sys.stdin.readlines()


stats = {}
for line in lines:
    for idx, c in enumerate(line.strip()):
        if idx not in stats:
            stats[idx] = {}

        if c not in stats[idx]:
            stats[idx][c] = 0

        stats[idx][c] += 1


max_letters = []
min_letters = []
for idx in sorted(stats.keys()):
    letter = max(stats[idx].keys(), key=lambda x: stats[idx][x])
    max_letters.append(letter)
    letter = min(stats[idx].keys(), key=lambda x: stats[idx][x])
    min_letters.append(letter)


print(stats)
print(''.join(max_letters))
print(''.join(min_letters))