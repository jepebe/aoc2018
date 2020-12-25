import intcode as ic

tester = ic.Tester('Crab Cups')


class dlist:
    class node:
        def __init__(self, value):
            self.value = value
            self.next_node = None
            self.prev_node = None

        def __str__(self):
            return f'node {self.value} p: {self.prev_node is None} n: {self.next_node is None}'

    def __init__(self):
        self.first = None
        self.last = None

    def __getitem__(self, item):
        if isinstance(item, int):
            if item < 0:
                raise IndexError

            node = self.first
            for i in range(item):
                node = node.next_node
                if node is None:
                    raise IndexError
            return node

    def __delitem__(self, node):
        prev_node = node.prev_node
        next_node = node.next_node
        if prev_node:
            prev_node.next_node = next_node
        else:
            self.first = next_node

        if next_node:
            next_node.prev_node = prev_node
        else:
            self.last = prev_node
        node.next_node = None
        node.prev_node = None

    def append(self, value):
        node = dlist.node(value)
        if self.first is None:
            self.first = node
            self.last = self.first
        else:
            node.prev_node = self.last
            self.last.next_node = node
            self.last = node
        return node

    def insert_after(self, node, new_node):
        next_node = node.next_node
        node.next_node = new_node
        new_node.prev_node = node
        new_node.next_node = next_node
        if next_node:
            next_node.prev_node = new_node
        else:
            self.last = new_node

    def rotate_left(self, n=1):
        for i in range(n):
            node = self.first
            self.first = self.first.next_node
            self.first.prev_node = None
            node.prev_node = self.last
            self.last.next_node = node
            self.last = node
            node.next_node = None

    def next_node(self, node, wrap_around=True):
        if node.next_node:
            return node.next_node
        elif wrap_around:
            return self.first
        else:
            return None

    def cut(self, from_node, to_node):
        prev_node = from_node.prev_node
        next_node = to_node.next_node
        if not prev_node:
            self.first = next_node
        else:
            prev_node.next_node = next_node

        if not next_node:
            self.last = prev_node
        else:
            next_node.prev_node = prev_node

    def move_segment(self, from_node, to_node, destination):
        self.cut(from_node, to_node)

        next_node = destination.next_node
        destination.next_node = from_node
        from_node.prev_node = destination
        to_node.next_node = next_node
        if not next_node:
            self.last = to_node
        else:
            next_node.prev_node = to_node

    def __iter__(self):
        node = self.first
        while node:
            yield node.value
            node = node.next_node

    def __str__(self):
        return ','.join(map(str, self))

    def __len__(self):
        count = 0
        node = self.first
        while node:
            count += 1
            node = node.next_node
        return count


def cups(n, moves=10, cups=9):
    arr = dlist()
    node_tracker = {}
    for v in map(int, n):
        node = arr.append(v)
        node_tracker[v] = node

    if cups > 9:
        for v in range(10, cups + 1):
            node = arr.append(v)
            node_tracker[v] = node

    curr = arr.first
    for i in range(moves):
        pa = arr.next_node(curr)
        pb = arr.next_node(pa)
        pc = arr.next_node(pb)
        dest = curr.value - 1
        while dest in (0, pa.value, pb.value, pc.value):
            dest -= 1
            if dest <= 0:
                dest = cups

        dest_node = node_tracker[dest]
        arr.move_segment(pa, pc, dest_node)
        curr = arr.next_node(curr)

    return arr, node_tracker


def simple_cups(n, moves=100):
    arr, node_tracker = cups(n, moves)
    node = arr.next_node(node_tracker[1])
    result = ''
    while node:
        if node.value == 1:
            break
        result += str(node.value)
        node = arr.next_node(node, wrap_around=True)
    return result


def mega_cups(n, moves=10000000):
    arr, node_tracker = cups(n, moves, cups=1000000)
    first = arr.next_node(node_tracker[1])
    second = arr.next_node(first)
    return first.value * second.value


tester.test_value(simple_cups('389125467', 10), '92658374')
tester.test_value(simple_cups('389125467'), '67384529')
tester.test_value(simple_cups('398254716'), '45798623', 'solution to part 1=%s')

tester.test_value(mega_cups('389125467'), 149245887792)
tester.test_value(mega_cups('398254716'), 235551949822, 'solution to part 2=%s')
