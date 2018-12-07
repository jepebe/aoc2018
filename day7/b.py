import sys

lines = sys.stdin.readlines()


# input CABDFGE

class Node(object):
    parent = []
    children = []


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

    node_duration = {node: 60 + ord(node) - ord('A') + 1 for node in nodes}

    return graph, dependency, nodes, node_duration


def find_independent(graph):
    keys = {key for key in graph.keys()}
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


def complete_graphs(graph, dependency):
    final_step = nodes.difference(graph.keys())

    graph[next(iter(final_step))] = []

    independent = find_independent(graph)
    for node in independent:
        dependency[node] = []


def free_worker(workers):
    time = workers['time']
    for id, worker in workers['workers'].items():
        if worker['queue'][time] == '.':
            return worker
    return None


def dedicate_worker(workers, worker, node):
    now = workers['time']
    duration = workers['cost'][node]

    worker['items'].append(node)
    for i in range(now, now + duration):
        worker['queue'][i] = node
    worker['time'] = now + duration


def step_workers(workers):
    workers['time'] += 1
    time = workers['time']

    for id, worker in workers['workers'].items():
        q = worker['queue']
        if q[time - 1] != '.' and q[time] == '.':
            workers['done'].append(q[time - 1])


def state(machine):
    for w in machine['workers']:
        print(''.join(machine['workers'][w]['queue']))


def queue(machine, node):
    if node in machine['processed']:
        return

    if node in machine['done']:
        return

    if node in machine['queue']:
        return

    machine['queue'].append(node)


def process(graph, dependency, machine):
    while len(machine['queue']) > 0:
        visited = []
        for node in machine['queue']:

            if free_worker(machine) and dependencies(dependency, node,
                                                     machine['done']):
                visited.append(node)
                machine['processed'].append(node)
                worker = free_worker(machine)
                dedicate_worker(machine, worker, node)

                for n in sorted(graph[node]):
                    queue(machine, n)

        for node in visited:
            machine['queue'].remove(node)

        if len(visited) == 0:
            step_workers(machine)


graph, dependency, nodes, node_duration = create_graph(lines)
complete_graphs(graph, dependency)

worst_case = sum(node_duration.values())


machine = {
    'time': 0,
    'cost': node_duration,
    'nodes': nodes,
    'processed': [],
    'done': [],
    'queue': sorted(find_independent(graph)),
    'workers':
        {
            1: {'id': 1, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            2: {'id': 2, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            # 3: {'id': 3, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            # 4: {'id': 4, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            # 5: {'id': 5, 'queue': ['.'] * worst_case, 'items': [], 'time': 0}
        }

}

process(graph, dependency, machine)

print(machine)

state(machine)


def dict_max(dct, key):
    max_id = 0
    max_value = 0
    for id, value in dct.items():
        if value[key] > max_value:
            max_id = id
            max_value = value[key]
    return dct[max_id]


print('max', dict_max(machine['workers'], 'time'))
