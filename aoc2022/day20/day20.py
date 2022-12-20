import typing

import aoc

tester = aoc.Tester("Grove Positioning System")


class Node:
    def __init__(self, value):
        self.value = value
        self._prev = None
        self._next = None

    @property
    def prev(self) -> typing.Self:
        return self._prev

    @prev.setter
    def prev(self, node):
        self._prev = node

    @property
    def next(self) -> typing.Self:
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = None
        self.next = None

    def insert_after(self, node):
        p = node.next
        node.next = self
        self.prev = node
        p.prev = self
        self.next = p

    def insert_before(self, node):
        p = node.prev
        node.prev = self
        self.next = node
        p.next = self
        self.prev = p

    @classmethod
    def print(cls, start: typing.Self, key=1):
        node = start
        while True:
            print(node.value * key, " ", end="")
            node = node.next
            if node == start:
                break
        print()


def parse_input(filename: str) -> list[Node]:
    data = aoc.read_input(filename)
    numbers = []
    for _, line in enumerate(data.splitlines()):
        n = Node(int(line))
        if numbers:
            n.prev = numbers[-1]
            numbers[-1].next = n
        numbers.append(n)
    numbers[0].prev = numbers[-1]
    numbers[-1].next = numbers[0]

    return numbers


def decrypt(numbers: list[Node], key=1) -> int:
    zero_node = None
    size = len(numbers)
    for node in numbers:
        value = node.value * key
        if value > 0:
            value = value % (size - 1)
            cur = node.next
            node.remove()
            for i in range(value - 1):
                cur = cur.next
            node.insert_after(cur)
        elif value < 0:
            value = (value % (size - 1)) - (size - 1)
            cur = node.prev
            node.remove()
            for i in range(value + 1, 0, 1):
                cur = cur.prev
            node.insert_before(cur)
        else:
            zero_node = node

    node = zero_node
    gps = 0
    for i in range(3):
        for _ in range(1000 % size):
            node = node.next
        gps += node.value * key

    return gps


def mix(numbers, key=811589153):
    for _ in range(10):
        gps = decrypt(numbers, key=key)
    return gps


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    numbers = parse_input("test_input")
    t.test_value(decrypt(numbers), 3)

    numbers = parse_input("test_input")
    t.test_value(mix(numbers), 1623178306)


run_tests(tester)

tester.test_section("Part 1")
gps = decrypt(parse_input("input"))
tester.test_value_neq(gps, -11641)
tester.test_value(gps, 3473, "solution to part 1=%s")

tester.test_section("Part 2")
gps = mix(parse_input("input"))
tester.test_value(gps, 7496649006261, "solution to part 2=%s")
