def create_orbits(lines):
    orbits = {}

    for line in lines:
        a, b = line.strip().split(')')
        if a not in orbits:
            orbits[a] = []
        orbits[a].append(b)
    return orbits


def orbit_count_checksum(orbits, node, depth=0):
    if node not in orbits:
        return depth

    orbitors = orbits[node]
    checksum = depth
    for orbitor in orbitors:
        checksum += orbit_count_checksum(orbits, orbitor, depth+1)
    return checksum


def find_parent(orbits, a):
    for parent, children in orbits.items():
        if a in children:
            return parent
    return None


def path_to_root(orbits, a):

    path = []
    parent = a
    while parent != 'COM':
        parent = find_parent(orbits, parent)
        path.append(parent)

    return path


def transfer_distance(orbits, a, b):
    path_a = path_to_root(orbits, a)
    path_b = path_to_root(orbits, b)

    return len(set(path_a) ^ set(path_b))


def load_test_data(filename):
    with open(filename) as f:
        orbits = create_orbits(f.readlines())
    return orbits, orbit_count_checksum(orbits, 'COM')


orbs, chksum = load_test_data('test')
assert chksum == 42

orbs, chksum = load_test_data('test2')
assert chksum == 54
assert transfer_distance(orbs, 'YOU', 'SAN') == 4

orbs, chksum = load_test_data('input')
assert chksum == 200001
assert transfer_distance(orbs, 'YOU', 'SAN') == 379
