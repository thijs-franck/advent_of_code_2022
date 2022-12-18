import re
from dataclasses import dataclass, field
from os import path
from typing import Dict, Iterable, Optional, Set

INPUT_PATH = path.join(path.dirname(__file__), "data")


@dataclass
class RegexParseException(Exception):
    input_string: str
# END RegexParseException


@dataclass
class Valve:
    label: str
    flow_rate: int
    neighbors: Set[str]

    opened: bool = False
# END Valve


@dataclass
class TunnelSystem:
    valves: Dict[str, Valve] = field(default_factory=dict)

    def get_valve(self, label: str) -> Optional[Valve]:
        return self.valves.get(label)
    # END get_valve

    def register_valve(self, valve: Valve):
        self.valves[valve.label] = valve
    # END register_valve

    @classmethod
    def from_valves(cls, valves: Iterable[Valve]):
        instance = cls()

        for valve in valves:
            instance.register_valve(valve)
        # END LOOP

        return instance
    # END from_valves
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


if __name__ == "__main__":
    valves = read_valves(INPUT_PATH)
    tunnel_system = TunnelSystem.from_valves(valves)

    starting_node = tunnel_system.get_valve("AA")

    print(starting_node)
# END IF
