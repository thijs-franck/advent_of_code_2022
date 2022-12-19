import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from os import path
from typing import Deque, Dict, Iterable, List, Optional, Set, Tuple

INPUT_PATH = path.join(path.dirname(__file__), "data")

Label = str
Path = List[str]


@dataclass
class RegexParseException(Exception):
    input_string: str
# END RegexParseException


@dataclass
class Valve:
    label: Label
    flow_rate: int
    neighbors: Set[Label]

    opened = False
# END Valve


@dataclass
class TunnelSystem:
    nodes: Dict[Label, Valve] = field(default_factory=dict)
    edges: Dict[Label, Set[Label]] = field(
        default_factory=lambda: defaultdict(set)
    )

    _shortest_paths: Dict[Label, Dict[Label, Path]] = field(
        default_factory=lambda: defaultdict(dict)
    )

    @classmethod
    def from_valves(cls, valves: Iterable[Valve]):
        instance = cls()

        for valve in valves:
            instance.register_node(valve)
            instance.register_edges(valve.label, valve.neighbors)
        # END LOOP

        return instance
    # END from_valves

    def current_flow_rate(self) -> int:
        return sum(valve.flow_rate for valve in self.nodes.values() if valve.opened)
    # END current_flow_rate

    def shortest_path(self, source: Label, target: Label) -> Path:

        if source in self._shortest_paths and target in self._shortest_paths[source]:
            return self._shortest_paths[source][target]
        # END IF

        if source == target:
            result: Path = []

            self._shortest_paths[source][target] = result
            self._shortest_paths[target][source] = result

            return result
        # END IF

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
                for label in self.edges[current_node]
                if label not in seen
            ]

            for label in edges:
                branch = list(path)
                branch.append(label)

                self._shortest_paths[source][label] = branch
                self._shortest_paths[label][source] = branch

                if label == target:
                    return branch
                # END IF

                paths.append(branch)
            # END LOOP

            seen.add(current_node)
        # END LOOP

        result = []

        self._shortest_paths[source][target] = result
        self._shortest_paths[target][source] = result

        return result
    # END shortest_path

    def get_node(self, label: str) -> Optional[Valve]:
        return self.nodes.get(label)
    # END get_node

    def register_edges(self, node: Label, edges: Set[Label]):
        self.edges[node] = edges
    # END register_edges

    def register_node(self, valve: Valve):
        self.nodes[valve.label] = valve
    # END register_node
# END TunnelSystem


def read_valves(path: str) -> Iterable[Valve]:

    PATTERN = r"^Valve (?P<label>[A-Z]+) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<neighbors>.*)$"

    with open(path) as file:

        lines = (line.rstrip("\n") for line in file)

        for line in lines:

            matches = re.match(PATTERN, line)

            if matches is None:
                raise RegexParseException(line)
            # END IF

            group_dict = matches.groupdict()
            neighbors = group_dict['neighbors'].split(", ")

            yield Valve(
                label=group_dict['label'],
                flow_rate=int(group_dict['flow_rate']),
                neighbors=set(neighbors)
            )
        # END LOOP
    # END WITH file
# END read_valves


def find_unblocked_valves(tunnel_system: TunnelSystem) -> Set[Label]:
    return {label for label, valve in tunnel_system.nodes.items() if valve.flow_rate > 0}
# END find_unblocked_valves


def dfs(tunnel_system: TunnelSystem, current_valve: Label, closed_valves: Set[Label], time_remaining: int, pressure_released: int = 0) -> Tuple[int, Path]:

    max_pressure_released: int = pressure_released
    optimal_path: Path = []

    for valve in closed_valves:

        path = tunnel_system.shortest_path(current_valve, valve)

        # A valve needs to be open for at least one minute to be of any effect
        if len(path) > (time_remaining - 2):
            continue
        # END IF

        flow_rate = tunnel_system.nodes[valve].flow_rate
        pressure_over_time = flow_rate * (time_remaining - len(path))

        valves_remaining = closed_valves.copy()
        valves_remaining.discard(valve)

        potential_pressure_released, _ = dfs(
            tunnel_system,
            valve,
            valves_remaining,
            time_remaining - len(path),
            pressure_released + pressure_over_time
        )

        if potential_pressure_released > max_pressure_released:
            max_pressure_released = potential_pressure_released
            optimal_path = path
        # END IF

    # END LOOP

    return max_pressure_released, optimal_path
# END dfs


@dataclass
class Worker:

    destination: Label
    tunnel_system: TunnelSystem
    valid_destinations: Set[Label]
    max_ticks: int

    ticks = 0
    ticks_remaining = 1

    def tick(self):
        self.ticks += 1
        self.ticks_remaining -= 1

        if self.ticks_remaining == 0:
            self.tunnel_system.nodes[self.destination].opened = True

            _, path = dfs(
                self.tunnel_system,
                self.destination,
                self.valid_destinations,
                self.max_ticks - self.ticks
            )

            if len(path) > 0:
                self.destination = path[-1]
                self.valid_destinations.discard(self.destination)
                self.ticks_remaining = len(path)
            # END IF
        # END IF
    # END tick
# END Worker


def find_max_pressure_release(tunnel_system: TunnelSystem, starting_valve: Label, n_workers: int, minutes: int):

    unblocked_valves = find_unblocked_valves(tunnel_system)
    workers = [
        Worker(starting_valve, tunnel_system, unblocked_valves, minutes)
        for _ in range(n_workers)
    ]
    pressure_released = 0

    for time_spent in range(minutes):

        for worker in workers:
            worker.tick()
        # END LOOP

        current_flow_rate = tunnel_system.current_flow_rate()
        pressure_released += current_flow_rate * (minutes - (time_spent + 1))
    # END LOOP

    return pressure_released
# END find_max_pressure_release


if __name__ == "__main__":
    valves = read_valves(INPUT_PATH)
    tunnel_system = TunnelSystem.from_valves(valves)

    max_pressure_release = find_max_pressure_release(
        tunnel_system, "AA", 2, 26)

    print(max_pressure_release)
# END IF
