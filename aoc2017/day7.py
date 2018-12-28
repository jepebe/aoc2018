def split(desc):
    values = desc.split()

    name = values[0]
    weight = int(values[1].replace('(', '').replace(')', ''))

    children = []

    if len(values) > 3:
        children = [child.replace(',', '') for child in values[3:]]

    return name, weight, children


def find_root(tower):
    weights = {}
    nodes = {}

    for line in tower:
        name, weight, children = split(line)
        weights[name] = weight
        nodes[name] = children

    has_parent = set()
    maybe_root = set()

    for node in nodes:
        children = nodes[node]

        if len(children) > 0:
            for child in children:
                has_parent.add(child)
        else:
            has_parent.add(node)

        if node not in has_parent:
            maybe_root.add(node)

    root = maybe_root - has_parent

    assert len(root) == 1

    return root.pop()


def calculate_branch(weights, nodes, node):
    children = nodes[node]
    if len(children) == 0:
        return weights[node]
    else:
        s = weights[node]
        for child in children:
            s += calculate_branch(weights, nodes, child)
        return s


def calculate_weights(root, lines):
    weights = {}
    nodes = {}

    for line in lines:
        name, weight, children = split(line)
        weights[name] = weight
        nodes[name] = children

    root_children = nodes[root]

    for node in root_children:
        w = calculate_branch(weights, nodes, node)
        print("%s (%d) -> %d" % (node, weights[node], w))


if __name__ == '__main__':
    assert split('pbga (66)') == ('pbga', 66, [])
    assert split('fwft (72) -> ktlj, cntj, xhth') == (
    'fwft', 72, ['ktlj', 'cntj', 'xhth'])

    with open('day7_test.txt', 'r') as f:
        lines = f.read().splitlines()

    assert find_root(lines) == 'tknk'
    calculate_weights('tknk', lines)

    with open('day7.txt', 'r') as f:
        lines = f.read().splitlines()

    print(find_root(lines))
    calculate_weights('dtacyn', lines)
    print('---')
    calculate_weights('xvuxc', lines)
    print('---')
    calculate_weights('nieyygi', lines)
    print('---')
    calculate_weights('ptshtrn', lines)
