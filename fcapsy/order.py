from collections import deque, namedtuple
from collections.abc import Mapping

from fcapsy import Concept
from fcapsy.algorithms.lindig import upper_neighbors
from fcapsy.algorithms.fcbo import fcbo


LatticeNode = namedtuple("LatticeNode", ["upper", "lower"])


class Lattice(Mapping):
    def __init__(self, context, algorithm='fcbo'):
        if algorithm == 'fcbo':
            self.__build_with_fcbo(context)
        else:
            self.__build_with_lindig(context)

    def __build_with_fcbo(self, context):
        """
        First, all concepts are calculated via FcBO algorithm, then they are ordered via
        Concepts Cover algorithm.

        Carpineto, Claudio, and Giovanni Romano. Concept data analysis: Theory and applications.
        John Wiley & Sons, 2004.
        """
        concepts = fcbo(context)

        self._mapping = dict(zip(concepts, [LatticeNode(
            upper=set(), lower=set()) for i in range(len(concepts))]))

        index = dict(zip([int(concept.extent)
                          for concept in concepts], concepts))

        for concept in concepts:
            counter = dict.fromkeys(concepts, 0)

            difference = context.Attributes.supremum - concept.intent

            for atom in context.Attributes.fromint(difference).atoms():
                intersection = concept.extent & context.down(atom)

                found_concept = index[intersection]
                counter[found_concept] += 1

                if (len(found_concept.intent) - len(concept.intent)) == counter[found_concept]:
                    self.get(concept).lower.add(found_concept)
                    self.get(found_concept).upper.add(concept)

    def __build_with_lindig(self, context):
        """
        Warning, this mode is slow!

        Based on Upper neighbor algorithm
        Lindig, Christian. "Fast concept analysis."
        Working with Conceptual Structures-Contributions to ICCS 2000 (2000): 152-161.
        """
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
