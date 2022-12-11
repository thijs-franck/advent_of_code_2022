from collections import ChainMap
from dataclasses import dataclass, field
from os import path
from typing import Dict, Iterable, Optional, Protocol

INPUT_PATH = path.join(path.dirname(__file__), "data")


class FileSystemElement(Protocol):
    name: str
    path: str
    size: int

    parent: Optional['Directory'] = None
# END FileSystemItem


@dataclass
class File:
    name: str
    size: int

    parent: Optional['Directory'] = None

    @property
    def path(self) -> str:
        path = ''

        if self.parent:
            path = self.parent.path
        # END IF

        return f'{path}/{self.name}'
    # END path
# END File


@dataclass
class Directory:
    name: str

    directories: Dict[str, 'Directory'] = field(default_factory=dict)
    files: Dict[str, File] = field(default_factory=dict)
    parent: Optional['Directory'] = None

    def get_directory(self, name: str):
        if name in self.directories:
            return self.directories[name]
        # END IF

        directory = Directory(name=name, parent=self)
        self.directories[name] = directory

        return directory
    # END get_directory

    def get_file(self, name: str, size: int):
        if name in self.files:
            return self.files[name]
        # END IF

        file = File(name=name, size=size, parent=self)
        self.files[name] = file

        return file
    # END get_file

    def tree(self):
        return ChainMap({self.path: self}, *(directory.tree() for directory in self.directories.values()))
    # END tree

    @property
    def size(self):
        return sum(child.size for child in self.children.values())
    # END size

    @property
    def children(self) -> ChainMap[str, FileSystemElement]:
        return ChainMap(self.directories, self.files)
    # END children

    @property
    def path(self) -> str:
        path = ''

        if self.parent:
            path = self.parent.path
        # END IF

        return f'{path}/{self.name}'
    # END path
# END Directory


def read_terminal_output(path: str) -> Iterable[str]:
    with open(path) as file:
        terminal_output = (line.rstrip('/n') for line in file)
        yield from terminal_output
    # END LOOP
# END read_terminal_output


def parse_terminal_output(terminal_output: Iterable[str]):
    root = Directory('')

    current_directory = root

    for output in terminal_output:
        tokens = output.split()

        # A line starting with $ indicates a command
        if tokens[0] == "$":
            command = tokens[1]
            if command == "cd":
                path = tokens[2]
                if path == "/":
                    current_directory = root
                elif path == "..":
                    if current_directory.parent is None:
                        continue
                    # END IF
                    current_directory = current_directory.parent
                else:
                    current_directory = current_directory.get_directory(path)
                # END IF
            # END IF
        else:
            if tokens[0] == "dir":
                continue
            # END IF

            size, name = tokens

            # Registers the file if not already known
            current_directory.get_file(name=name, size=int(size))
        # END IF
    # END LOOP

    return root
# END parse_terminal_output


if __name__ == "__main__":
    terminal_output = read_terminal_output(INPUT_PATH)
    file_system = parse_terminal_output(terminal_output)

    print(
        sum(
            directory.size
            for directory in file_system.tree().values()
            if directory.size <= 100000
        )
    )
# END IF
