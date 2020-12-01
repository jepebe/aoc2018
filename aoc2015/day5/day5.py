import intcode as ic


def naughty(word):
    naughty_set = {'ab', 'cd', 'pq', 'xy'}
    vowel_count = 0
    double_letter = 0
    prev_c = None
    for c in word:
        if c in 'aeiou':
            vowel_count += 1
        if prev_c and prev_c == c:
            double_letter += 1
        if prev_c and f'{prev_c}{c}' in naughty_set:
            return True
        prev_c = c
    return not (vowel_count >= 3 and double_letter > 0)


def improved_naughty(word):
    pairs = {}
    nice_pair = 0
    repeat = 0
    for i, c in enumerate(word):
        if i > 0:
            pair = f'{word[i - 1]}{c}'
            if pair not in pairs:
                pairs[pair] = i
            if i - pairs[pair] > 1:
                nice_pair += 1
        if i > 1:
            if word[i - 2] == c:
                repeat += 1
    return not (nice_pair > 0 and repeat > 0)


tester = ic.Tester("naughty strings")

tester.test_value(naughty('ugknbfddgicrmopn'), False)
tester.test_value(naughty('aaa'), False)
tester.test_value(naughty('jchzalrnumimnmhp'), True)
tester.test_value(naughty('haegwjzuvuyypxyu'), True)
tester.test_value(naughty('dvszwmarrgswjxmb'), True)

tester.test_value(improved_naughty('qjhvhtzxzqqjkmpb'), False)
tester.test_value(improved_naughty('xxyxx'), False)
tester.test_value(improved_naughty('uurcxstgmygtbstg'), True)
tester.test_value(improved_naughty('ieodomkazucvgmuy'), True)

with open("input") as f:
    data = f.readlines()

nice = 0
improved_nice = 0
for line in data:
    if not naughty(line):
        nice += 1

    if not improved_naughty(line):
        improved_nice += 1

tester.test_value(nice, 258)
tester.test_value(improved_nice, 53)
