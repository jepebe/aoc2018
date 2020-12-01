import intcode as ic


def wrapping(w, h, l):
    a = w * h
    b = w * l
    c = h * l
    m = min(a, b, c)
    return a * 2 + b * 2 + c * 2 + m


def ribbon(w, h, l):
    a, b, _ = sorted((w, h, l))
    ribbon = a * 2 + b * 2
    bow = w * h * l
    return ribbon + bow


tester = ic.Tester('wrapping')

tester.test_value(wrapping(2, 3, 4), 58)
tester.test_value(wrapping(1, 1, 10), 43)

tester.test_value(ribbon(2, 3, 4), 34)
tester.test_value(ribbon(1, 1, 10), 14)

with open('input') as f:
    data = f.readlines()

wrapping_sum = 0
ribbon_sum = 0
for line in data:
    w, h, l = tuple(map(int, line.split("x")))
    wrapping_sum += wrapping(w, h, l)
    ribbon_sum += ribbon(w, h, l)

tester.test_value(wrapping_sum, 1598415)
tester.test_value(ribbon_sum, 3812909)

print(f'the elves need {wrapping_sum} square feet of wrapping paper')
print(f'the elves need {ribbon_sum} feet of ribbon')

tester.summary()
