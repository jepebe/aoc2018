import re

import intcode as ic

tester = ic.Tester('Monster Messages')


def read_file(postfix=''):
    with open(f'input{postfix}') as f:
        lines = f.readlines()
    return lines


def cmp_letter(c):
    def fn(rules, d):
        return c
    return fn


def or_rule(left, right):
    def fn(rules, d):
        if d == 14:
            return ''

        left_group = []
        for r in left:
            left_group.append(rules[r](rules, d + 1))

        right_group = []
        for r in right:
            right_group.append(rules[r](rules, d + 1))
        return f'({"".join(left_group)}|{"".join(right_group)})'

    return fn


def uber_rule(indexes):
    def fn(rules, d):
        rule = []
        for idx in indexes:
            rule.append(rules[idx](rules, d + 1))
        return ''.join(rule)

    return fn


def parse(lines):
    rules = {}
    messages = []

    rule_mode = True
    for line in lines:
        if not line.strip():
            rule_mode = False
            continue

        if rule_mode:
            n, rule = line.split(': ')
            n = int(n)

            if '"' in rule:
                c = rule.strip().replace('"', '')
                rules[n] = cmp_letter(c)
            elif '|' in rule:
                left, right = rule.split('|')
                left = tuple(map(int, left.strip().split(' ')))
                right = tuple(map(int, right.strip().split(' ')))
                rules[n] = or_rule(left, right)
            else:
                idx = tuple(map(int, rule.split(' ')))
                rules[n] = uber_rule(idx)
        else:
            messages.append(line.strip())
    return rules, messages


def evaluate(rules, message):
    r = rules[0](rules, 0)
    regex = re.compile(f'^{r}$')
    return regex.match(message) is not None


def evaluate_all(rules, messages):
    count = 0
    r = rules[0](rules, 0)
    # print(r)
    regex = re.compile(f'^{r}$')
    for message in messages:
        if regex.match(message) is not None:
            count += 1
    return count


lines = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".splitlines()

rules, messages = parse(lines)
tester.test_value(evaluate(rules, 'ababbb'), True)
tester.test_value(evaluate(rules, 'bababa'), False)
tester.test_value(evaluate(rules, 'abbbab'), True)
tester.test_value(evaluate(rules, 'aaabbb'), False)
tester.test_value(evaluate(rules, 'aaaabbb'), False)

tester.test_value(evaluate_all(rules, messages), 2)

rules, messages = parse(read_file())
tester.test_value(evaluate_all(rules, messages), 224, 'solution to part 1=%s')

rules, messages = parse(read_file(postfix='_test'))
tester.test_value(evaluate_all(rules, messages), 3)
rules[8] = or_rule((42,), (42, 8))
rules[11] = or_rule((42, 31), (42, 11, 31))
tester.test_value(evaluate_all(rules, messages), 12)

rules, messages = parse(read_file())
rules[8] = or_rule((42,), (42, 8))
rules[11] = or_rule((42, 31), (42, 11, 31))
tester.test_value(evaluate_all(rules, messages), 436, 'solution to part 2=%s')
