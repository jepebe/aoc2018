import intcode as ic


def sumify(string):
    result = 0

    number = ''
    for c in string:

        if c.isnumeric():
            number += c
        elif not number and c == '-':
            number += '-'
        else:
            if len(number) > 0 and number != '-':
                result += int(number)
                number = ''

    return result


tester = ic.Tester("JSAbacusFramework.io")

tester.test_value(sumify('[1,2,3]'), 6)
tester.test_value(sumify('{"a":2,"b":4}'), 6)
tester.test_value(sumify('[[[3]]]'), 3)
tester.test_value(sumify('{"a":{"b":4},"c":-1}'), 3)
tester.test_value(sumify('{"a":[-1,1]}'), 0)
tester.test_value(sumify('[-1,{"a":1}]'), 0)
tester.test_value(sumify('[]'), 0)
tester.test_value(sumify('{}'), 0)

with open('input') as f:
    data = f.read()

tester.test_value(sumify(data), 119433, 'solution to exercise 1 = %s')
