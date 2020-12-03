import intcode as ic


def parse(line):
    rule, passwd = line.split(':')
    f_t, c = rule.split(' ')
    f, t = f_t.split('-')
    return int(f), int(t), c, passwd.strip()


def validate_password(frm, to, char, password):
    return frm <= password.count(char) <= to


def validate_password_indexed(frm, to, char, password):
    a = password[frm - 1] == char
    b = password[to - 1] == char
    return (a or b) and not (a and b)


def validate_passwords(lines):
    count = 0
    count_indexed = 0
    for line in lines:
        if validate_password(*parse(line.strip())):
            count += 1
        if validate_password_indexed(*parse(line.strip())):
            count_indexed += 1
    return count, count_indexed


tester = ic.Tester("Password Philosophy")

data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

tester.test_value(validate_passwords(data.strip().split('\n')), (2, 1))

with open('input') as f:
    lines = f.readlines()

valid_passwords = validate_passwords(lines)
tester.test_value(valid_passwords, (477, 686), "solution to exercise 1=%s and 2=%s")
