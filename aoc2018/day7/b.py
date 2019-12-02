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


def find_free_worker(workers):
    time = workers['time']
    for worker in workers['workers'].values():
        if worker['queue'][time] == '.':
            return worker
    return None


def dedicate_worker(workers, worker, node):
    now = workers['time']
    duration = workers['cost'][node]

    worker['queue'][now:now + duration] = [node] * duration
    worker['time'] = now + duration


def step_workers(workers):
    workers['time'] += 1
    time = workers['time']

    for worker in workers['workers'].values():
        q = worker['queue']
        if q[time - 1] != '.' and q[time] == '.':
            workers['done'].append(q[time - 1])


def queue(machine, node):
    if node in machine['processed']:
        return

    if node in machine['done']:
        return

    if node in machine['queue']:
        return

    machine['queue'].append(node)


def all_deps_done(machine, node):
    return all([n in machine['done'] for n in machine['graph'][node]['p']])


def process(machine):
    while len(machine['queue']) > 0:
        visited = []
        for node in machine['queue']:
            worker = find_free_worker(machine)

            if worker and all_deps_done(machine, node):
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
        {n: {'id': n, 'queue': ['.'] * worst_case, 'time': 0} for n in range(3)}
}

process(machine)

print(machine)


def print_state(machine):
    for w in machine['workers']:
        print(''.join(machine['workers'][w]['queue']))


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
