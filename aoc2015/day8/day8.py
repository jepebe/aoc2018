import intcode as ic


def pack(string):
    code = 0
    content = 0
    escape = 0
    re_escape = 0
    for c in string:
        code += 1
        re_escape += 1
        if not escape and c == '\\':
            escape = 1
            re_escape += 1
        elif escape and c in ('"', '\\'):
            content += 1
            escape -= 1
            re_escape += 1
        elif escape and c == 'x':
            content += 1
            escape = 2
        elif escape:
            escape -= 1
        elif c != '"':
            content += 1
        elif c == '"':
            re_escape += 2

    return code, content, re_escape


tester = ic.Tester("Matchsticks")

tester.test_value(pack('""'), (2, 0, 6))
tester.test_value(pack('"abc"'), (5, 3, 9))
tester.test_value(pack('"aaa\\"aaa"'), (10, 7, 16))
tester.test_value(pack('"\\x27"'), (6, 1, 11))


with open('input') as f:
    lines = f.readlines()

code_sum = 0
content_sum = 0
re_escape_sum = 0

for line in lines:
    cod, cnt, resc = pack(line)
    code_sum += cod
    content_sum += cnt
    re_escape_sum += resc


tester.test_value(code_sum - content_sum, 1342)
tester.test_value(re_escape_sum - code_sum, 2074)
