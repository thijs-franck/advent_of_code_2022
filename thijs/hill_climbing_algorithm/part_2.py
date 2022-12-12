from collections import defaultdict, deque
from dataclasses import dataclass, field
from os import path
from typing import Callable, Deque, Dict, List, Set, Tuple
from uuid import uuid4

INPUT_PATH = path.join(path.dirname(__file__), "data")

Label = str
Elevation = str
Weight = int
Edge = Tuple[Label, Weight]
WeightFunction = Callable[[Elevation, Elevation], Weight]
WeightPredicate = Callable[[Weight], bool]
Path = List[Label]


@dataclass
class Node:
    elevation: Elevation
    label: Label = field(default_factory=lambda: str(uuid4()))
# END Node

TargetPredicate = Callable[[Node], bool]

@dataclass
class Graph:
    weight_function: WeightFunction

    nodes: Dict[Label, Node] = field(default_factory=dict)

    edges: Dict[Label, Set[Edge]] = field(
        default_factory=lambda: defaultdict(set)
    )

    def add_node(self, node: Node):
        self.nodes[node.label] = node
    # END add_node

    def add_edge(self, source: Label, target: Label):
        weight = self.weight_function(
            self.nodes[source].elevation,
            self.nodes[target].elevation
        )
        edge = (target, weight)
        self.edges[source].add(edge)
    # add_edge
# END Graph


def init_graph(path: str, graph: Graph):
    with open(path) as file:
        rows = (line.rstrip("\n") for line in file)

        def create_node(elevation: Elevation):
            node = None
            if elevation == "S":
                node = Node("a", "S")
            elif elevation == "E":
                node = Node("z", "E")
            else:
                node = Node(elevation)
            # END IF
            return node
        # END create_node

        previous = None

        for row in rows:
            current = [create_node(elevation) for elevation in row]

            for index, node in enumerate(current):
                graph.add_node(node)

                if index > 0:
                    graph.add_edge(node.label, current[index - 1].label)
                    graph.add_edge(current[index - 1].label, node.label)
                # END IF

                if previous is not None:
                    graph.add_edge(node.label, previous[index].label)
                    graph.add_edge(previous[index].label, node.label)
                # END IF
            # END LOOP

            previous = current
        # END LOOP
    # END WITH file

    return graph
# END init_graph


def weight_function(source: Elevation, target: Elevation):
    return ord(target) - ord(source)
# END weight_function


def weight_predicate(weight: Weight):
    return weight <= 1
# END weight_predicate

def target_predicate(node: Node):
    return node.elevation == 'a'
# END target_predicate


def shortest_path(graph: Graph, source: Label, target_predicate: TargetPredicate, weight_predicate: WeightPredicate) -> Path:

    seen: Set[Label] = set()
    paths: Deque[Path] = deque([[source]])

    while len(paths) > 0:

        path = paths.popleft()
        current_node = path[-1]

        if current_node in seen:
            continue
        # END IF

        edges = [
            label
            for label, weight in graph.edges[current_node]
            if label not in seen and weight_predicate(weight)
        ]

        for label in edges:
            branch = list(path)
            branch.append(label)

            if target_predicate(graph.nodes[label]):
                return branch
            # END IF

            paths.append(branch)
        # END LOOP

        seen.add(current_node)
    # END LOOP

    return []
# END shortest_path


if __name__ == "__main__":
    graph = Graph(weight_function=weight_function)

    init_graph(INPUT_PATH, graph)

    result = shortest_path(graph, "E", target_predicate, weight_predicate)

    print(len(result) - 1)
# END MAIN
