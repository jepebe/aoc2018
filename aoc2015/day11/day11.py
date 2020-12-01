import intcode as ic

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def valid(password):
    password = [alphabet.index(c) for c in password]
    return _valid(password)


def _valid(password):
    nums = []
    asc_rule = False
    pairs = set()
    for i, c in enumerate(password):
        if c in (8, 11, 14):
            return False

        if not asc_rule and i >= 2:
            asc_rule = c - 1 == nums[i - 1] == nums[i - 2] + 1
        if i >= 1:
            if c == nums[i - 1]:
                pairs.add(c)

        nums.append(c)

    if len(pairs) >= 2:
        pair_rule = True
    else:
        pair_rule = False

    return asc_rule and pair_rule


def inc_password(password):
    for i in range(7, -1, -1):
        password[i] += 1
        if password[i] >= len(alphabet):
            password[i] = 0
        else:
            break


def next_password(password):
    password = [alphabet.index(c) for c in password]
    inc_password(password)
    while not _valid(password):
        inc_password(password)

    return ''.join([alphabet[c] for c in password])


tester = ic.Tester("Corporate Policy")

tester.test_value(valid("hijklmmn"), False)
tester.test_value(valid("abbceffg"), False)
tester.test_value(valid("abbcegjk"), False)
tester.test_value(valid("abcdefgh"), False)

tester.test_value(valid("abcdaaaa"), False)
tester.test_value(valid("abcdffaa"), True)
tester.test_value(valid("ghijklmn"), False)
tester.test_value(valid("ghjaabcc"), True)
print("--- Next password tests ---")
tester.test_value(next_password("abcdefgh"), "abcdffaa")
tester.test_value(next_password("ghijklmn"), "ghjaabcc")

tester.test_value(next_password("vzbxkghb"), "vzbxxyzz", 'solution for exercise 1 = %s')
tester.test_value(next_password("vzbxxyzz"), "vzcaabcc", 'solution for exercise 2 = %s')
