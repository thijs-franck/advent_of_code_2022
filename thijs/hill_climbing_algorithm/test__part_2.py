from os import path

from .part_2 import (Graph, init_graph, shortest_path, weight_function, target_predicate,
                     weight_predicate)

INPUT_PATH = path.join(path.dirname(__file__), "sample_data")


def test__shortest_path():

    graph = Graph(weight_function)

    init_graph(INPUT_PATH, graph)

    result = shortest_path(graph, "E", target_predicate, weight_predicate)

    assert len(result) -1 == 29
# END test__shortest_path
