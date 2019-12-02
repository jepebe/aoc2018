import sys

lines = sys.stdin.readlines()


def parse_input(lines):
    pots = None
    rules = {}
    for line in lines:
        if line.strip() == '':
            continue

        if line.startswith('initial'):
            initial_state = line.strip()[15:]
            pots = [c for c in initial_state]
        else:
            from_state, to_state = line.strip().split(' => ')
            rules[from_state] = to_state
    return pots, rules


pots, rules = parse_input(lines)


def run_generation(pots, rules, zero):
    result = []
    for i in range(-1, len(pots) + 1):
        pattern = []
        for p in range(-2, 3):
            if i + p < 0 or i + p >= len(pots):
                pattern.append('.')
            else:
                pattern.append(pots[i + p])

        pattern = ''.join(pattern)

        if pattern in rules:
            ptrn = rules[pattern]
            if i < 0:
                zero += 1

            result.append(ptrn)
        else:
            if 0 <= i < len(pots):
                result.append('.')

    print(''.join(result), sum(i - zero for i, x in enumerate(result) if x == '#'), zero)

    return result, zero

#print(pots)
#print(rules)

zero = 0
score = 0
for gen in range(3):
    pots, zero = run_generation(pots, rules, zero)
    new_score = sum(i - zero for i, x in enumerate(pots) if x == '#')
    #print(gen, new_score, new_score - score)
    score = new_score

print(sum(i - zero for i, x in enumerate(pots) if x == '#'))

# input converges at a diff of 26

print('200 -->', 5011 + (200 - 167) * 26)
print('201 -->', 5011 + (201 - 167) * 26)
print('50000000000 -->', 5011 + (50000000000 - 167) * 26)


