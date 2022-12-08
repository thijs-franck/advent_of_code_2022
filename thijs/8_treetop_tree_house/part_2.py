from dataclasses import dataclass, field
from math import prod
from os import path
from typing import List

INPUT_PATH = path.join(path.dirname(__file__), "data")


@dataclass
class Tree:
    forest: 'Forest'
    x: int
    y: int
    z: int

    def scenic_score(self):
        dimensions = list(self.forest.get_neighbors(self))
        viewing_distance = []
        for dimension in dimensions:
            for index, tree in enumerate(dimension):
                if tree.z < self.z:
                    continue
                # END IF

                viewing_distance.append(index + 1)
                break
            else:
                viewing_distance.append(len(dimension))
            # END LOOP
        # END LOOP
        return prod(viewing_distance)
    # END scenic_score
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

        def reverse(trees: List[Tree]) -> List[Tree]:
            trees.reverse()
            return trees
        # END reverse

        yield reverse([tree for tree in self.trees[tree.y][:tree.x]])
        yield [tree for tree in self.trees[tree.y][tree.x + 1:]]
        yield reverse([col[tree.x] for col in self.trees[:tree.y]])
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
    max_score = max(tree.scenic_score() for tree in forest)

    print(max_score)
# END IF
