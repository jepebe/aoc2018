def create_graph(lines):
    graph = {}
    for line in lines:
        f, t = line.split('/')

        f = int(f)
        t = int(t)

        if f not in graph:
            graph[f] = []

        if t not in graph:
            graph[t] = []

        graph[f].append(t)
        graph[t].append(f)
    return graph


def score(edges):
    return sum((a + b for a, b in edges))


def dfs(graph, edges, visit):
    neighbours = graph[visit]

    #print(edges)

    if len(neighbours) == 1:
        return score(edges), (len(edges), score(edges))

    scores = []

    for n in neighbours:
        f = min(visit, n)
        t = max(visit, n)

        if (f, t) not in edges:
            scores.append(dfs(graph, edges + [(f, t)], n))

    if len(scores) == 0:
        return score(edges), (len(edges), score(edges))

    max_score = 0
    lng, lscr = (0, 0)
    for scr, (l, s) in scores:
        max_score = max(max_score, scr)

        if l > lng or (l == lng and s > lscr):
            lng = l
            lscr = s

    return max_score, (lng, lscr)


if __name__ == '__main__':
    with open('day24_test.txt', 'r') as f:
        lines = f.readlines()

    assert len(lines) == len({line for line in lines})
    g = create_graph(lines)
    print(g)

    print(dfs(g, [], 0))

    with open('day24.txt', 'r') as f:
        lines = f.readlines()

    g = create_graph(lines)
    assert len(lines) == len({line for line in lines})
    print(dfs(g, [], 0))
