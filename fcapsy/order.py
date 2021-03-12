from collections import deque, namedtuple
from collections.abc import Mapping

from fcapsy import Concept
from fcapsy.algorithms.lindig import upper_neighbors


LatticeNode = namedtuple("LatticeNode", ["upper", "lower"])


class Lattice(Mapping):
    """
    Based on Upper neighbor algorithm
    Lindig, Christian. "Fast concept analysis."
    Working with Conceptual Structures-Contributions to ICCS 2000 (2000): 152-161.
    """

    def __init__(self, context):
        self._mapping = {}

        init_intent = context.Attributes.supremum
        init_extent = context.down(init_intent)

        init_concept = Concept(init_extent, init_intent)

        self._mapping[init_concept] = LatticeNode(
            upper=set(), lower=set())

        queue = deque((init_concept, ))

        while queue:
            concept = queue.pop()

            for neighbor in upper_neighbors(context, concept):
                existing_neighbor = self.get(neighbor)

                if not existing_neighbor:
                    self._mapping[neighbor] = LatticeNode(
                        upper=set(), lower={concept, })
                else:
                    existing_neighbor.lower.add(concept)

                self[concept].upper.add(neighbor)

                queue.append(neighbor)

    def __getitem__(self, concept: Concept):
        return self._mapping[concept]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    @property
    def concepts(self) -> tuple:
        return tuple(self.keys())
