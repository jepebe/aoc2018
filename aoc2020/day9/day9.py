import intcode as ic

tester = ic.Tester('Encoding Error')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return map(int, lines)


def x_mas_sum(s, numbers):
    for i, a in enumerate(numbers):
        for b in numbers[i:]:
            if a + b == s:
                return True
    return False


def xmas(numbers, preamble=5):
    for i in range(preamble, len(numbers)):
        s = numbers[i]
        if not x_mas_sum(s, numbers[i - preamble:i]):
            return s
    return None


def contiguous(value, numbers):
    numbers = list(numbers)
    size = len(numbers)
    a = 0
    b = 2
    while b < size:
        s = sum(numbers[a:b])
        if s > value:
            a += 1
        elif s < value:
            b += 1
        elif s == value:
            return min(numbers[a:b]) + max(numbers[a:b])


lines = map(int, """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split('\n'))
lines = list(lines)
tester.test_value(xmas(lines), 127)
tester.test_value(contiguous(127, lines), 62)

lines = read_file()
lines = list(lines)
tester.test_value(xmas(lines, preamble=25), 1038347917, 'solution to exercise 1=%s')
tester.test_value(contiguous(1038347917, lines), 137394018, 'solution to exercise 2=%s')
