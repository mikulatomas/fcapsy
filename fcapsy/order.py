import json
from multiprocessing import cpu_count

from collections import deque, namedtuple, OrderedDict
from collections.abc import Mapping

from fcapsy import Concept
from fcapsy.algorithms.lindig import upper_neighbors
from fcapsy.algorithms.concepts_cover import concept_cover, concept_cover_parallel
from fcapsy.algorithms.fcbo import fcbo


LatticeNode = namedtuple("LatticeNode", ["upper", "lower"])


class Lattice(Mapping):
    def __init__(self, mapping):
        sorted_mapping = OrderedDict(
            sorted(mapping.items(), key=lambda c: c[0].extent.shortlex()))
        self._mapping = sorted_mapping

    @classmethod
    def from_context(cls, context, algorithm='concept_cover', n_of_workers=1):
        if algorithm == 'concept_cover':
            mapping = cls.concept_cover_mapping(context, n_of_workers)
        elif algorithm == 'lindig':
            mapping = cls.lindig_mapping(context)
        else:
            raise ValueError('Unknow algorithm for building concept lattice.')

        return cls(mapping)

    @ staticmethod
    def concept_cover_mapping(context, n_of_workers=1):
        """
        First, all concepts are calculated via FcBO algorithm, then they are ordered via
        Concepts Cover algorithm.

        Carpineto, Claudio, and Giovanni Romano. Concept data analysis: Theory and applications.
        John Wiley & Sons, 2004.
        """
        concepts = fcbo(context)

        mapping = dict(zip(concepts, [LatticeNode(
            upper=set(), lower=set()) for i in range(len(concepts))]))

        if n_of_workers > 1:
            edges = concept_cover_parallel(concepts, context, n_of_workers)
        else:
            edges = concept_cover(concepts, context)

        for concept, lower_neighbor in edges:
            mapping[concept].lower.add(lower_neighbor)
            mapping[lower_neighbor].upper.add(concept)

        return mapping

    @ staticmethod
    def lindig_mapping(context):
        """
        Warning, this mode is slow!

        Based on Upper neighbor algorithm
        Lindig, Christian. "Fast concept analysis."
        Working with Conceptual Structures-Contributions to ICCS 2000 (2000): 152-161.
        """
        mapping = {}

        init_intent = context.Attributes.supremum
        init_extent = context.down(init_intent)

        init_concept = Concept(init_extent, init_intent)

        mapping[init_concept] = LatticeNode(
            upper=set(), lower=set())

        queue = deque((init_concept, ))

        while queue:
            concept = queue.pop()

            for neighbor in upper_neighbors(context, concept):
                existing_neighbor = mapping.get(neighbor)

                if not existing_neighbor:
                    mapping[neighbor] = LatticeNode(
                        upper=set(), lower={concept, })
                else:
                    existing_neighbor.lower.add(concept)

                mapping[concept].upper.add(neighbor)

                queue.append(neighbor)

        return mapping

    @classmethod
    def from_json(cls, filename, context):
        with open(filename, 'r') as f:
            lattice_dict = json.load(f)

        concepts = dict(zip(
            map(int, lattice_dict.keys()),
            (Concept.from_intent(context.Attributes.fromint(intent), context) for intent in lattice_dict.keys())))

        mapping = dict(zip(
            concepts.values(),
            [LatticeNode(upper=set(), lower=set()) for i in range(len(concepts))]))

        for concept, upper_neighbors_intents in zip(mapping.keys(), lattice_dict.values()):
            for intent in upper_neighbors_intents:
                neighbor = concepts[intent]
                mapping[concept].upper.add(neighbor)
                mapping[neighbor].lower.add(concept)

        return cls(mapping)

    def to_json(self, filename):
        lattice_dict = dict(zip(
            map(lambda concept: int(concept.intent), self._mapping.keys()),
            map(lambda node: tuple(map(lambda concept: int(concept.intent), node.upper)), self._mapping.values())))

        with open(filename, 'w') as f:
            json.dump(lattice_dict, f)

    def __getitem__(self, concept: Concept):
        return self._mapping[concept]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    @ property
    def concepts(self) -> tuple:
        return tuple(self.keys())
