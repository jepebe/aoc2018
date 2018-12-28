def process(data):
    group_score = 0
    garbage_count = 0
    stack =[]
    garbage = False
    ignore = False

    for c in data:
        if ignore:
            ignore = False
            continue

        if c == '{' and not garbage:
            stack.append(len(stack) + 1)
        elif c == '}' and not garbage:
            group_score += stack.pop()
        elif c == '<' and not garbage:
            garbage = True
        elif c == '>' and garbage:
            garbage = False
        elif c == '!':
            ignore = True
        elif garbage:
            garbage_count += 1

    assert len(stack) == 0
    return group_score, garbage_count


if __name__ == '__main__':
    assert process('<>') == (0, 0)
    assert process('<random characters>') == (0, 17)
    assert process('<<<<>') == (0, 3)
    assert process('<{!>}>') == (0, 2)
    assert process('<!!>') == (0, 0)
    assert process('<!!!>>') == (0, 0)
    assert process('<{o"i!a,<{i<a>') == (0, 10)
    assert process('{}') == (1, 0)
    assert process('{{{}}}') == (6, 0)
    assert process('{{{},{},{{}}}}') == (16, 0)
    assert process('{<a>,<a>,<a>,<a>}') == (1, 4)
    assert process('{{<a>},{<a>},{<a>},{<a>}}') == (9, 4)
    assert process('{{<!>},{<!>},{<!>},{<a>}}') == (3, 13)
    assert process('{{<!!>},{<!!>},{<!!>},{<!!>}}') == (9, 0)

    with open('day9.txt', 'r') as f:
        data = f.read()

    print(process(data))
