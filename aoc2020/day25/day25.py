import intcode as ic

tester = ic.Tester('Combo Breaker')


def transform(subject, size):
    value = 1
    for i in range(size):
        value *= subject
        value = value % 20201227

    return value


def find_loop_size(key):
    value = 1
    i = 0
    while True:
        i += 1
        value *= 7
        value = value % 20201227
        if value == key:
            return i


tester.test_value(find_loop_size(17807724), 11)
tester.test_value(find_loop_size(5764801), 8)

tester.test_value(transform(17807724, 8), 14897079)
tester.test_value(transform(5764801, 11), 14897079)

loop_size_b = find_loop_size(15065270)
tester.test_value(transform(17607508, loop_size_b), 12285001, 'solution to part 1=%s')
loop_size_a = find_loop_size(17607508)
tester.test_value(transform(15065270, loop_size_a), 12285001)




