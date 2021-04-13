import json
from multiprocessing import Process, Queue, cpu_count
from queue import Empty

from collections import deque, namedtuple
from collections.abc import Mapping

from fcapsy import Concept
from fcapsy.algorithms.lindig import upper_neighbors
from fcapsy.algorithms.fcbo import fcbo


LatticeNode = namedtuple("LatticeNode", ["upper", "lower"])


class Lattice(Mapping):
    def __init__(self, mapping):
        self._mapping = mapping

    @classmethod
    def from_context(cls, context, algorithm='fcbo', number_of_workers=cpu_count()):
        if algorithm == 'fcbo':
            mapping = cls.build_mapping_with_fcbo(context)
        elif algorithm == 'fcbo_parallel':
            mapping = cls.build_mapping_with_fcbo_parallel(
                context, number_of_workers)
        elif algorithm == 'lindig':
            mapping = cls.build_mapping_with_lindig(context)
        else:
            raise ValueError('Unknow algorithm for building concept lattice.')

        return cls(mapping)

    @ staticmethod
    def build_mapping_with_fcbo(context):
        """
        First, all concepts are calculated via FcBO algorithm, then they are ordered via
        Concepts Cover algorithm.

        Carpineto, Claudio, and Giovanni Romano. Concept data analysis: Theory and applications.
        John Wiley & Sons, 2004.
        """
        concepts = fcbo(context)

        mapping = dict(zip(concepts, [LatticeNode(
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
                    mapping[concept].lower.add(found_concept)
                    mapping[found_concept].upper.add(concept)

        return mapping

    @staticmethod
    def calculate_mapping_parallel(concept_chunk_indexes, context, index, queue):
        concepts = tuple(index.values())

        for concept in concepts[concept_chunk_indexes[0]:concept_chunk_indexes[1]]:
            counter = dict.fromkeys(concepts, 0)
            difference = context.Attributes.supremum - concept.intent

            for atom in context.Attributes.fromint(difference).atoms():
                intersection = concept.extent & context.down(atom)

                found_concept = index[intersection]
                counter[found_concept] += 1

                if (len(found_concept.intent) - len(concept.intent)) == counter[found_concept]:
                    queue.put((concept, found_concept))

        queue.put(False)

    @ staticmethod
    def build_mapping_with_fcbo_parallel(context, number_of_workers):
        """
        Parallel version of `build_mapping_with_fcbo()`.
        """

        def split_indexes(a, n):
            k, m = divmod(len(a), n)
            return ((i * k + min(i, m), (i + 1) * k + min(i + 1, m)) for i in range(n))

        concepts = fcbo(context)

        mapping = dict(zip(concepts, [LatticeNode(
            upper=set(), lower=set()) for i in range(len(concepts))]))

        concept_chunks_indexes = tuple(
            split_indexes(concepts, number_of_workers))

        index = dict(zip([int(concept.extent)
                          for concept in concepts], concepts))

        proces_queue_pairs = []

        for concept_chunk_indexes in concept_chunks_indexes:
            queue = Queue()
            process = Process(target=Lattice.calculate_mapping_parallel, args=(
                concept_chunk_indexes, context, index, queue))

            proces_queue_pairs.append((process, queue))

        for process, _ in proces_queue_pairs:
            process.start()

        n_of_finished_workers = 0

        while n_of_finished_workers != number_of_workers:
            for process, queue in proces_queue_pairs:
                try:
                    result = queue.get(block=False)

                    if not result:
                        n_of_finished_workers += 1
                        break

                    concept, lower_neighbor = result

                    mapping[concept].lower.add(lower_neighbor)
                    mapping[lower_neighbor].upper.add(concept)
                except Empty:
                    pass

        for process, _ in proces_queue_pairs:
            process.join()

        return mapping

    @ staticmethod
    def build_mapping_with_lindig(context):
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
