import sys

lines = sys.stdin.readlines()


# input CABDFGE


def create_graph(lines):
    graph = {}
    for line in lines:
        before = line[5]
        after = line[36]

        if before not in graph:
            graph[before] = {'id': before, 'p': [], 'c': []}

        graph[before]['c'].append(after)

        if after not in graph:
            graph[after] = {'id': after, 'p': [], 'c': []}

        graph[after]['p'].append(before)

    roots = []
    for key, value in graph.items():
        if len(value['p']) == 0:
            roots.append(key)

    return graph, sorted(roots)


def dependencies_finished(node, done):
    deps = node['p']
    for n in deps:
        if n not in done:
            return False
    return True


def find_free_worker(workers):
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


def print_state(machine):
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


def process(graph, machine):
    while len(machine['queue']) > 0:
        visited = []
        for node in machine['queue']:
            worker = find_free_worker(machine)
            if worker and dependencies_finished(graph[node], machine['done']):
                visited.append(node)
                machine['processed'].append(node)
                dedicate_worker(machine, worker, node)

                for n in sorted(graph[node]['c']):
                    queue(machine, n)

        for node in visited:
            machine['queue'].remove(node)

        if len(visited) == 0:
            step_workers(machine)


graph, roots = create_graph(lines)
node_duration = {node: 0 + ord(node) - ord('A') + 1 for node in graph.keys()}
worst_case = sum(node_duration.values())

machine = {
    'time': 0,
    'cost': node_duration,
    'processed': [],
    'done': [],
    'graph': graph,
    'queue': roots,
    'workers':
        {
            1: {'id': 1, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            2: {'id': 2, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            # 3: {'id': 3, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            # 4: {'id': 4, 'queue': ['.'] * worst_case, 'items': [], 'time': 0},
            # 5: {'id': 5, 'queue': ['.'] * worst_case, 'items': [], 'time': 0}
        }
}

process(graph, machine)

print(machine)

print_state(machine)


def dict_max(dct, key):
    max_id = 0
    max_value = 0
    for id, value in dct.items():
        if value[key] > max_value:
            max_id = id
            max_value = value[key]
    return dct[max_id]


print('max', dict_max(machine['workers'], 'time')['time'])
