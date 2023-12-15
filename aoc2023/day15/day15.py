import aoc

tester = aoc.Tester("Lens Library")


def parse(data: str):
    seqs = []
    for seq in data.split(","):
        seqs.append(seq)
    return seqs


def HASH(seq: str) -> int:
    h = 0
    for c in seq:
        h = h + ord(c)
        h *= 17
        h = h % 256
    return h


def hashify(sequences: list[str]) -> int:
    sum_hash = 0
    for seq in sequences:
        sum_hash += HASH(seq)

    return sum_hash


def hashmap(sequences: list[str]) -> int:
    hashmap = {}
    for seq in sequences:
        if "=" in seq:
            label, value = seq.split("=")
            box = HASH(label)
            if box in hashmap:
                found = False
                for i, (l, v) in enumerate(hashmap[box]):
                    if l == label:
                        hashmap[box][i] = (label, int(value))
                        found = True
                        break
                if not found:
                    hashmap[box].append((label, int(value)))
            else:
                hashmap[box] = [(label, int(value))]
        elif "-" in seq:
            label = seq[:-1]
            box = HASH(label)
            if box in hashmap:
                for i, (l, v) in enumerate(hashmap[box]):
                    if l == label:
                        del hashmap[box][i]
                        break

    focusing_power = 0
    for box, labels in hashmap.items():
        box += 1
        box_power = 0
        for index, (_, value) in enumerate(labels, start=1):
            box_power += box * index * value
        focusing_power += box_power
    return focusing_power


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = parse(aoc.read_input("input_test"))
    t.test_value(hashify(data), 1320)
    t.test_value(hashmap(data), 145)


run_tests(tester)

data = aoc.read_input()
sequences = parse(data)

tester.test_section("Part 1")
solution_1 = hashify(sequences)
tester.test_solution(solution_1, 517315)

tester.test_section("Part 2")
solution_2 = hashmap(sequences)
tester.test_solution(solution_2, 247763)
