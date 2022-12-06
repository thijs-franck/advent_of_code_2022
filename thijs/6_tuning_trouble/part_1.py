from dataclasses import dataclass
from os import path
from typing import Callable, Iterable

INPUT_PATH = path.join(path.dirname(__file__), 'data')


Position = int
Signal = str
PacketScanner = Callable[[Signal, Position, Position], bool]


@dataclass
class SignalReader:
    packet_scanner: PacketScanner
    signal: Signal
    index: Position = 0
    start_of_packet: Position = 0

    def read_packets(self) -> Iterable[str]:
        while(self.index < len(self.signal)):
            if self.packet_scanner(self.signal, self.start_of_packet, self.index):
                yield self.signal[self.start_of_packet: self.index]
                self.start_of_packet = self.index
            # END IF
            self.index += 1
        # END LOOP
    # END read_packets
# END SignalReader


def packet_scanner(signal: Signal, start_of_packet: Position, index: Position):
    if index - start_of_packet < 4:
        return False
    # END IF
    segment = signal[index-4:index]
    return len(set(segment)) == 4
# END packet_scanner


def read_signal(path: str):
    with open(path) as file:
        return file.read()
    # END WITH file
# END read_signal


if __name__ == "__main__":

    signal = read_signal(INPUT_PATH)

    reader = SignalReader(packet_scanner, signal)

    first_packet = next(reader.read_packets())

    print(len(first_packet))
    print(first_packet)
# END MAIN
