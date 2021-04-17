import json
from multiprocessing import cpu_count

from collections import deque, namedtuple

from fcapsy import Concept, Context
from fcapsy.algorithms.lindig import superordinate_concepts
from fcapsy.algorithms.concepts_cover import concept_cover, concept_cover_parallel
from fcapsy.algorithms.fcbo import fcbo


ConceptHierarchyNode = namedtuple(
    "ConceptHierarchyNode", ["superordinate", "subordinate"])


class ConceptHierarchy():
    def __init__(self, context, concepts, mapping):
        self.context = context
        self.concepts = tuple(sorted(concepts,
                                     key=lambda concept: concept.extent.longlex()))

        self._mapping = {}

        for concept, neighbours in mapping.items():
            self._mapping[concept] = ConceptHierarchyNode(superordinate=frozenset(neighbours.superordinate),
                                                          subordinate=frozenset(neighbours.subordinate))

    @classmethod
    def from_concepts(cls, concepts, context, n_of_workers=1):
        mapping = cls.concept_cover_hierarchy(
            concepts, context, n_of_workers)
        return cls(context, concepts, mapping)

    @classmethod
    def from_context(cls, context, algorithm='concept_cover', n_of_workers=1):
        if algorithm == 'concept_cover':
            concepts = fcbo(context)
            mapping = cls.concept_cover_hierarchy(
                concepts, context, n_of_workers)
        elif algorithm == 'lindig':
            concepts, mapping = cls.lindig_hierarchy(context)
        else:
            raise ValueError(
                'Unknow algorithm for building concept hierarchy.')

        return cls(context, concepts, mapping)

    @classmethod
    def from_pandas(cls, dataframe, name: str = None, n_of_workers=1):
        context = Context.from_pandas(dataframe, name=name)

        return cls.from_context(context, n_of_workers=n_of_workers)

    @staticmethod
    def concept_cover_hierarchy(concepts, context, n_of_workers=1):
        """
        First, all concepts are calculated via FcBO algorithm, then they are ordered via
        Concepts Cover algorithm.

        Carpineto, Claudio, and Giovanni Romano. Concept data analysis: Theory and applications.
        John Wiley & Sons, 2004.
        """

        mapping = dict(zip(concepts, [ConceptHierarchyNode(
            superordinate=set(), subordinate=set()) for i in range(len(concepts))]))

        if n_of_workers > 1:
            edges = concept_cover_parallel(concepts, context, n_of_workers)
        else:
            edges = concept_cover(concepts, context)

        for concept, subordinate_concept in edges:
            mapping[concept].subordinate.add(subordinate_concept)
            mapping[subordinate_concept].superordinate.add(concept)

        return mapping

    @staticmethod
    def lindig_hierarchy(context):
        """
        Warning, this mode is slow!

        Based on Lindig algorithm
        Lindig, Christian. "Fast concept analysis."
        Working with Conceptual Structures-Contributions to ICCS 2000 (2000): 152-161.
        """
        mapping = {}

        init_intent = context.Attributes.supremum
        init_extent = context.down(init_intent)

        init_concept = Concept(init_extent, init_intent)

        mapping[init_concept] = ConceptHierarchyNode(
            superordinate=set(), subordinate=set())

        queue = deque((init_concept, ))

        while queue:
            concept = queue.pop()

            for superordinate in superordinate_concepts(context, concept):
                existing_superordinate = mapping.get(superordinate)

                if not existing_superordinate:
                    mapping[superordinate] = ConceptHierarchyNode(
                        superordinate=set(), subordinate={concept, })
                else:
                    existing_superordinate.subordinate.add(concept)

                mapping[concept].superordinate.add(superordinate)

                queue.append(superordinate)

        return list(mapping.keys()), mapping

    @classmethod
    def from_json(cls, filename, context):
        with open(filename, 'r') as f:
            hierarchy_dict = json.load(f)

        concepts_index = {}
        concepts = []

        for intent in hierarchy_dict.keys():
            concept = Concept.from_intent(context.Attributes.fromint(
                int(intent)), context)

            concepts.append(concept)
            concepts_index[int(intent)] = concept

        mapping = dict(zip(
            concepts,
            [ConceptHierarchyNode(superordinate=set(), subordinate=set()) for i in range(len(concepts))]))

        for concept, superordinate_concepts_intents in zip(mapping.keys(), hierarchy_dict.values()):
            for intent in superordinate_concepts_intents:
                superordinate = concepts_index[intent]
                mapping[concept].superordinate.add(superordinate)
                mapping[superordinate].subordinate.add(concept)

        return cls(context, concepts, mapping)

    def to_json(self, filename):
        hierarchy_dict = dict(zip(
            map(lambda concept: int(concept.intent), self._mapping.keys()),
            map(lambda node: tuple(map(lambda concept: int(concept.intent), node.superordinate)), self._mapping.values())))

        with open(filename, 'w') as f:
            json.dump(hierarchy_dict, f)

    def __len__(self):
        return len(self.concepts)

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return ((self.context == other.context) and
                    (self.concepts == other.concepts) and
                    (self._mapping == other._mapping))

    def __repr__(self):
        return "ConceptHierarchy({})".format(len(self.concepts))

    @property
    def top(self):
        return self.concepts[0]

    @property
    def bottom(self):
        return self.concepts[-1]

    def superordinate(self, concept):
        return self._mapping[concept].superordinate

    def subordinate(self, concept):
        return self._mapping[concept].subordinate
