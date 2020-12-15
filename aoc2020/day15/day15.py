import intcode as ic

tester = ic.Tester('Rambunctious Recitation')


# this is the Reddit version of the solution (twice as fast as mine)
def speak(nums, until):
    spoken = {n: i + 1 for i, n in enumerate(nums)}
    last = nums[-1]
    for i in range(len(nums) + 1, until + 1):
        s = i - 1 - spoken[last] if last in spoken else 0
        spoken[last] = i - 1
        last = s
    return last


puzzle_input = (0, 13, 16, 17, 1, 10, 6)
part_1 = 2020
part_2 = 30000000

tester.test_value(speak((0, 3, 6), 4), 0)
tester.test_value(speak((0, 3, 6), 5), 3)
tester.test_value(speak((0, 3, 6), 6), 3)
tester.test_value(speak((0, 3, 6), 7), 1)
tester.test_value(speak((1, 3, 2), part_1), 1)
tester.test_value(speak((2, 1, 3), part_1), 10)
tester.test_value(speak((1, 2, 3), part_1), 27)
tester.test_value(speak((2, 3, 1), part_1), 78)
tester.test_value(speak((3, 2, 1), part_1), 438)
tester.test_value(speak((3, 1, 2), part_1), 1836)
tester.test_value(speak(puzzle_input, part_1), 276, 'solution to part 1=%s')

# tester.test_value(speak((0, 3, 6), part_2), 175594)
tester.test_value(speak(puzzle_input, part_2), 31916, 'solution to part 2=%s')
