import collections
import typing

Distances: typing.TypeAlias = dict[tuple[str, str], int]


def floyd_warshall(valves: dict[str, dict]) -> Distances:
    # find distances between all vertices all neighbors have weight 1
    dist = collections.defaultdict(lambda: 99999999)
    for u, data in valves.items():
        for v in data["neighbors"]:
            dist[(u, v)] = 1
            dist[(v, u)] = 1
            dist[(u, u)] = 0

    for k in valves.keys():
        for i in valves.keys():
            for j in valves.keys():
                if dist[(i, j)] > (dist[(i, k)] + dist[(k, j)]):
                    dist[(i, j)] = (dist[(i, k)] + dist[(k, j)])

    return dist


def print_floyd_warshall(keys: typing.Iterable, dist: Distances):
    print("   ", end="")
    for x in keys:
        print(f"{x:2} ", end="")
    print()

    for y in keys:
        print(f"{y} ", end="")
        for x in keys:
            v = dist[(x, y)]
            print(f"{v:2} ", end="")
        print()
