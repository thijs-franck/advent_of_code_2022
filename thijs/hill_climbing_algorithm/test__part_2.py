from os import path

from .part_2 import (Graph, init_graph, shortest_path, weight_function,
                     weight_predicate)

INPUT_PATH = path.join(path.dirname(__file__), "sample_data")


def test__shortest_path():

    graph = Graph(weight_function)

    init_graph(INPUT_PATH, graph)

    nodes_marked_a = (
        label for label, node in graph.nodes.items() if node.elevation == "a")

    paths = [
        shortest_path(graph, label, "E", weight_predicate)
        for label in nodes_marked_a
    ]

    result = min(len(path) for path in paths if len(path) > 0)

    assert result - 1 == 29
# END test__shortest_path
