from os import path

from .part_1 import (Graph, init_graph, shortest_path, weight_function, target_predicate,
                     weight_predicate)

INPUT_PATH = path.join(path.dirname(__file__), "sample_data")


def test__shortest_path():

    graph = Graph(weight_function)

    init_graph(INPUT_PATH, graph)

    result = shortest_path(graph, "S", target_predicate, weight_predicate)

    assert len(result) - 1 == 31
# END test__shortest_path
