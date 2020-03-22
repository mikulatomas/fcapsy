from fcapy import Concept
from collections import deque
from itertools import combinations
from functools import reduce


class Lattice:
    def __init__(self, context):
        self._UPPER = 'upper'
        self._LOWER = 'lower'
        self._CONCEPT = 'concept'
        self._lattice = {}

        init_intent = context._Attributes.supremum
        init_extent = context._Objects.fromint(context.down(init_intent))

        init_concept = Concept(init_extent, init_intent)

        self._lattice[init_concept.get_id()] = {
            self._UPPER: set(), self._LOWER: set(), self._CONCEPT: init_concept}

        queue = deque((init_concept, ))

        while queue:
            concept = queue.pop()

            for neighbor in self.__calculate_upper_neighbors(context, concept):
                existing_neighbor = self._lattice.get(neighbor.get_id())

                if not existing_neighbor:
                    self._lattice[neighbor.get_id()] = {
                        self._UPPER: set(), self._LOWER: set((concept, )), self._CONCEPT: neighbor}
                else:
                    existing_neighbor[self._LOWER].add(concept)

                self._lattice[concept.get_id()][self._UPPER].add(neighbor)

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
        neighbors = self._lattice.get(concept.get_id())

        if not neighbors:
            raise ValueError('Concept is not in lattice.')

        return neighbors

    def get_upper(self, concept):
        return self.__get_neighbors(concept).get(self._UPPER)

    def get_lower(self, concept):
        return self.__get_neighbors(concept).get(self._LOWER)

    def get_concept_by_id(self, idx):
        return self._lattice[idx][self._CONCEPT]

    def get_concepts(self):
        return tuple(map(lambda x: x[self._CONCEPT], self._lattice.values()))


# Experimental
class SubsetLattice:
    def __init__(self, context, similarity_measure):
        self._UPPER = 'upper'
        self._LOWER = 'lower'
        self._CONCEPT = 'concept'
        self._subset_lattice = {}

        Objects = context._Objects
        Attributes = context._Attributes

        init_intent = context._Attributes.supremum
        init_extent = context._Objects.fromint(context.down(init_intent))

        init_concept = Concept(init_extent, init_intent)

        atoms = Objects.supremum.atoms()

        worklist = set([Concept(Objects.fromint(context.down(context.up(extent))),
                                Attributes.fromint(context.up(extent))) for extent in atoms])

        self._subset_lattice[init_concept.get_id()] = {
            self._UPPER: worklist.copy(), self._LOWER: set(), self._CONCEPT: init_concept}

        # add worklist to subset lattice
        for atom in worklist:
            self._subset_lattice[atom.get_id()] = {
                self._UPPER: set(), self._LOWER: set([init_concept]), self._CONCEPT: atom}
        while len(worklist) > 1:
            concept_combinations = tuple(combinations(worklist, 2))

            distances = [1 - similarity_measure(
                concepts[0].intent, concepts[1].intent) for concepts in concept_combinations]

            min_distance = min(distances)

            found = set()

            for concept_tuple, distance in zip(concept_combinations, distances):
                if distance == min_distance:
                    found.add(concept_tuple[0])
                    found.add(concept_tuple[1])

            worklist = worklist.difference(found)

            extent = reduce(lambda c1, c2: c1 | c2,
                            map(lambda x: x.extent, found))

            new_intent = context.up(extent)
            new_extent = context.down(new_intent)

            new_concept = Concept(Objects.fromint(
                new_extent), Attributes.fromint(new_intent))

            existing_neighbor = self._subset_lattice.get(
                new_concept.get_id())

            for concept in found:
                if not existing_neighbor:
                    self._subset_lattice[new_concept.get_id()] = {
                        self._UPPER: set(), self._LOWER: set((concept, )), self._CONCEPT: new_concept}
                else:
                    existing_neighbor[self._LOWER].add(concept)

                self._subset_lattice[concept.get_id()][self._UPPER].add(
                    new_concept)

            worklist.add(new_concept)

    def __get_neighbors(self, concept):
        neighbors = self._subset_lattice.get(concept.get_id())

        if not neighbors:
            raise ValueError('Concept is not in subset lattice.')

        return neighbors

    def get_upper(self, concept):
        return self.__get_neighbors(concept).get(self._UPPER)

    def get_lower(self, concept):
        return self.__get_neighbors(concept).get(self._LOWER)

    def get_concept_by_id(self, idx):
        return self._subset_lattice[idx][self._CONCEPT]

    def get_concepts(self):
        return tuple(map(lambda x: x[self._CONCEPT], self._subset_lattice.values()))
