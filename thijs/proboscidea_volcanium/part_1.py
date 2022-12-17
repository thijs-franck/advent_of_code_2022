import re
from dataclasses import dataclass
from typing import Iterable, Set


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


def read_valves(path: str) -> Iterable[Valve]:

    PATTERN = r"Valve (?P<label>[A-Z]+) has flow rate=(?P<flow_rate>\d+); tunnels lead to valves (?P<neighbors>.*)"

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


