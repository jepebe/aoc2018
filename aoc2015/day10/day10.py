import intcode as ic


def look_and_say(seq):
    result = ''
    count = 0
    prev = None
    for c in seq:
        if prev is None:
            prev = c
            count = 1
        elif c == prev:
            count += 1
        else:
            result += f'{count}{prev}'
            prev = c
            count = 1

    if prev:
        result += f'{count}{prev}'

    return result


tester = ic.Tester("look-and-say")

tester.test_value(look_and_say('1'), '11')
tester.test_value(look_and_say('11'), '21')
tester.test_value(look_and_say('21'), '1211')
tester.test_value(look_and_say('1211'), '111221')
tester.test_value(look_and_say('111221'), '312211')

seq = '3113322113'
for i in range(40):
    seq = look_and_say(seq)

tester.test_value(len(seq), 329356, 'solution to exercise 1 = %s')

seq = '3113322113'
for i in range(50):
    seq = look_and_say(seq)

tester.test_value(len(seq), 4666278, 'solution to exercise 2 = %s')
