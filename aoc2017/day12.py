def connect(graph, frm, to):
    if frm not in graph:
        graph[frm] = set()

    if to not in graph:
        graph[to] = set()

    graph[frm].add(to)
    graph[to].add(frm)


def build_graph(lines):
    graph = {}
    for line in lines:
        frm, to = line.split(' <-> ')
        to = [int(t) for t in to.split(', ')]
        frm = int(frm)

        for t in to:
            connect(graph, frm, t)
    print(graph)
    return graph


def group(graph, id):
    v = set()
    q = [id]

    while q:
        id = q.pop()
        v.add(id)

        q.extend([n for n in graph[id] if n not in v])

    return v


def count_groups(graph):
    v = set()
    groups = []

    for n in graph:
        if n not in v:
            grp = group(graph, n)
            groups.append(grp)
            v.update(grp)

    return len(groups)


if __name__ == '__main__':
    with open('day12_test.txt', 'r') as f:
        lines = f.readlines()

    grph = build_graph(lines)

    assert grph[0] == {2}
    assert grph[6] == {4, 5}

    assert len(group(grph, 0)) == 6
    assert count_groups(grph) == 2

    with open('day12.txt', 'r') as f:
        lines = f.readlines()

    grph = build_graph(lines)
    print(len(group(grph, 0)))
    print(count_groups(grph))
