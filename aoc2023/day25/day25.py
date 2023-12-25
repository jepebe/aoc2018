import aoc
import networkx as nx

tester = aoc.Tester("Snowverload")


def parse(data: str) -> nx.Graph:
    graph = nx.Graph()
    for line in data.splitlines():
        source, dest = line.split(":")
        dest = dest.strip().split(" ")
        graph.add_node(source)
        for d in dest:
            graph.add_edge(source, d)

    return graph


def snowverload(graph: nx.Graph) -> int:
    for n1 in graph.nodes:
        for n2 in graph.nodes:
            if n1 == n2:
                continue
            cut = nx.minimum_edge_cut(graph, n1, n2)
            if len(cut) == 3:
                for edge in cut:
                    graph.remove_edge(edge[0], edge[1])

                comp = list(nx.connected_components(graph))
                return len(comp[0]) * len(comp[1])


def run_tests(t: aoc.Tester):
    t.test_section("Tests")
    data = aoc.read_input("input_test")
    g = parse(data)

    # failed to make Kargers terminate for input, resolved to use networkx :(

    t.test_value(snowverload(g), 54)


run_tests(tester)

data = aoc.read_input()
graph = parse(data)

tester.test_section("Part 1")
solution_1 = snowverload(graph)
tester.test_solution(solution_1, 538368)
