def is_valid(num):
    nums = list(map(int, str(num)))
    for i in range(5):
        if nums[i + 1] < nums[i]:
            return False
    if len(set(nums)) < 6:
        return True
    return False


assert is_valid(111111) is True
assert is_valid(223450) is False
assert is_valid(123789) is False


def is_valid_2(num):
    nums = list(map(int, str(num)))
    hist = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for i in nums:
        hist[i] += 1

    for i in range(5):
        if nums[i + 1] < nums[i]:
            return False

    if len(set(nums)) == 6:
        return False

    double = False
    for i in range(9, -1, -1):
        if hist[i] == 2:
            double = True
    return double


assert is_valid_2(112233) is True
assert is_valid_2(123444) is False
assert is_valid_2(111122) is True

count_1 = 0
count_2 = 0
for i in range(153517, 630395 + 1):

    if is_valid(i):
        count_1 += 1
    if is_valid_2(i):
        count_2 += 1

assert count_1 == 1729
assert count_2 == 1172
print(count_1, count_2)
