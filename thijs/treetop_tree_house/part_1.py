from dataclasses import dataclass, field
from os import path
from typing import List

INPUT_PATH = path.join(path.dirname(__file__), "data")


@dataclass
class Tree:
    forest: 'Forest'
    x: int
    y: int
    z: int

    def is_visible(self):
        """
        Returns `True` if this tree is visible from any side of the forest
        """

        def visible_from_dimension(dimension: List[Tree]):
            return all(tree.z < self.z for tree in dimension)
        # END visible_from_dimension

        return any(visible_from_dimension(dimension) for dimension in self.forest.get_neighbors(self))
    # END is_visible
# END Tree


@dataclass
class Forest:
    trees: List[List[Tree]] = field(default_factory=list)

    def __iter__(self):
        """
        Iterates over all trees in the forest

        :yield: A tree in this forest
        :rtype: Tree
        """
        for col in self.trees:
            yield from col
        # END LOOP
    # END __iter__

    def get_neighbors(self, tree: Tree):
        yield [tree for tree in self.trees[tree.y][:tree.x]]
        yield [tree for tree in self.trees[tree.y][tree.x + 1:]]
        yield [col[tree.x] for col in self.trees[:tree.y]]
        yield [col[tree.x] for col in self.trees[tree.y + 1:]]
    # END get_neighbors

    def add_tree(self, x: int, y: int, z: int):
        if len(self.trees) == y:
            self.trees.append([])
        # END IF

        tree = Tree(self, x, y, z)

        self.trees[y].append(tree)

        return tree
    # END add_tree
# END Forest


def read_forest(path: str):
    forest = Forest()

    with open(path) as file:
        rows = (row.rstrip('\n') for row in file)
        for y, row in enumerate(rows):
            for x, z in enumerate(row):
                forest.add_tree(int(x), int(y), int(z))
            # END LOOP
        # END LOOP
    # END WITH file

    return forest
# END read_forest


if __name__ == '__main__':
    forest = read_forest(INPUT_PATH)
    visible_trees = [tree for tree in forest if tree.is_visible()]

    print(len(visible_trees))
# END IF
