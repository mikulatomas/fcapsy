from fcapy import Concept
from collections import deque


class Lattice:
    def __init__(self, context):
        self._UPPER = 'upper'
        self._LOWER = 'lower'
        self._lattice = {}

        init_intent = context._Attributes.supremum
        init_extent = context._Objects.fromint(context.down(init_intent))

        init_concept = Concept(init_extent, init_intent)

        self._lattice[init_concept] = {self._UPPER: set(), self._LOWER: set()}

        queue = deque((init_concept, ))

        while queue:
            concept = queue.pop()

            for neighbor in self.__calculate_upper_neighbors(context, concept):
                existing_neighbor = self._lattice.get(neighbor)

                if not existing_neighbor:
                    self._lattice[neighbor] = {
                        self._UPPER: set(), self._LOWER: set((concept, ))}
                else:
                    existing_neighbor[self._LOWER].add(concept)

                self._lattice[concept][self._UPPER].add(neighbor)

                queue.append(neighbor)

    def __calculate_upper_neighbors(self, context, concept):
        minimal = ~concept.extent

        for objects in context._Objects.atomic(minimal):
            new_intent = context.up(concept.extent | objects)
            new_extent = context.down(new_intent)

            if minimal & (new_extent & ~objects):
                minimal &= ~objects
            else:
                neighbor = Concept(
                    context._Objects.fromint(new_extent),
                    context._Attributes.fromint(new_intent))

                yield neighbor

    def __get_neighbors(self, concept):
        neighbors = self._lattice.get(concept)

        if not neighbors:
            raise ValueError('Concept is not in lattice.')

        return neighbors

    def get_upper(self, concept):
        return self.__get_neighbors(concept).get(self._UPPER)

    def get_lower(self, concept):
        return self.__get_neighbors(concept).get(self._LOWER)

    def get_concepts(self):
        return tuple(self._lattice.keys())
