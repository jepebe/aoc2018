import itertools

import intcode as ic


def fit(containers, amount):
    count = 0
    container_count = {}
    min_container_count = len(containers)
    for comb in itertools.product([0, 1], repeat=len(containers)):
        if sum([c for i, c in enumerate(containers) if comb[i]]) == amount:
            count += 1
            cnt = sum(comb)

            if cnt < min_container_count:
                min_container_count = cnt

            if cnt not in container_count:
                container_count[cnt] = 0
            container_count[cnt] += 1

    return count, container_count[min_container_count]


tester = ic.Tester("No Such Thing as Too Much")

containers = [20, 15, 10, 5, 5]

tester.test_value(fit(containers, 25), (4, 3))

containers = [33, 14, 18, 20, 45, 35, 16, 35, 1, 13,
              18, 13, 50, 44, 48, 6, 24, 41, 30, 42]

tester.test_value(fit(containers, 150), (1304, 18), 'solution to exercise 1 = %s and 2 = %s')
