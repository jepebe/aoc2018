from itertools import combinations


class chip:
    def __init__(self, name):
        self.name = name

    def compatible(self, other):
        return isinstance(other, gen) and self.name == other.name

    def memo(self):
        return self.name[0:2] + 'm'


class gen:
    def __init__(self, name):
        self.name = name

    def compatible(self, other):
        return isinstance(other, chip) and self.name == other.name

    def memo(self):
        return self.name[0:2] + 'g'


def memo(floors, floor):
    m = '%s' % floor
    for floor in floors:
        for item in sorted(floor, key=lambda x: x.name):
            m += item.memo()
        m += ','
    return m


def safe(floors, floor):
    return True


def copy_floors(floors):
    return [floors[0][:], floors[1][:], floors[2][:], floors[3][:]]

input = [
    [gen('promethium'), chip('promethium')],
    [gen('cobalt'), gen('curium'), gen('ruthenium'), gen('plutonium')],
    [chip('cobalt'), chip('curium'), chip('ruthenium'), chip('plutonium')],
    []
]

test = [
    [chip('hydrogen'), chip('lithium')],
    [gen('hydrogen')],
    [gen('lithium')],
    []
]

floors = test

item_count = sum([len(row) for row in floors])

states = []


def move(floors, floor):
    #state = memo(floors, floor)
    #
    #if state in states:
    #    print('Pruned')
    #    return None
    #elif not safe(floors, floor):
    #    return None
    #el
    if len(floors[3]) == item_count:
        #print('-->', state)
        return 1
    #else:
    #    states.append(state)

    minimum = []
    for item in floors[floor]:
        cpf = copy_floors(floors)
        cpf[floor].remove(item)

        if floor + 1 < 4:
            cpf[floor + 1].append(item)
            minimum.append(move(cpf, floor + 1))
            cpf[floor + 1].remove(item)

        if floor - 1 >= 0:
            cpf[floor - 1].append(item)
            minimum.append(move(cpf, floor - 1))

    for item in combinations(floors[floor], 2):
        cpf = copy_floors(floors)
        cpf[floor].remove(item[0])
        cpf[floor].remove(item[1])

        if floor + 1 < 4:
            cpf[floor + 1].append(item[0])
            cpf[floor + 1].append(item[1])
            minimum.append(move(cpf, floor + 1))
            cpf[floor + 1].remove(item[0])
            cpf[floor + 1].remove(item[1])

        if floor - 1 >= 0:
            cpf[floor - 1].append(item[0])
            cpf[floor - 1].append(item[1])
            minimum.append(move(cpf, floor - 1))

    minimum = min([x for x in minimum if x is not None], default=None)
    return minimum + 1 if minimum is not None else None

    # take one, take two, move up, move down

minimum = move(floors, 0)

print(states)
print(item_count, minimum)
