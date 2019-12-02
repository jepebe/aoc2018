import sys

lines = sys.stdin.readlines()


# input CABDFGE

def create_graph(lines):
    graph = {}
    dependency = {}
    nodes = set()
    for line in lines:
        before = line[5]
        after = line[36]

        nodes.add(before)
        nodes.add(after)

        if before not in graph:
            graph[before] = []

        graph[before].append(after)

        if after not in dependency:
            dependency[after] = []

        dependency[after].append(before)

    return graph, dependency, nodes


def find_independent(graph):
    keys = {key for key in graph.keys()}
    # print(keys)
    for key in list(keys):
        for items in graph.values():
            if key in items:
                keys.remove(key)
                break
    return sorted(list(keys))


def dependencies(dependency, node, done):
    deps = dependency[node]
    for node in deps:
        if node not in done:
            return False
    return True


def traverse(graph, dependency, nodes, done):
    for node in sorted(nodes):
        if node not in done and dependencies(dependency, node, done):
            done.append(node)
            traverse(graph, dependency, graph[node], done)
    return done


graph, dependency, nodes = create_graph(lines)

final_step = nodes.difference(graph.keys())

graph[next(iter(final_step))] = []

independent = find_independent(graph)
for node in independent:
    dependency[node] = []

traversal = traverse(graph, dependency, independent, [])

print(graph)
print(dependency)

print(final_step)

print(independent)
print(''.join(traversal))
