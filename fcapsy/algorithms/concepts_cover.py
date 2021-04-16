from multiprocessing import Process, Queue, cpu_count
from queue import Empty


def _yield_edge(concept_index, context, from_idx=None, to_idx=None):
    concepts = tuple(concept_index.values())

    if from_idx is None and to_idx is None:
        from_idx = 0
        to_idx = len(concepts)

    for concept in concepts[from_idx:to_idx]:
        counter = dict.fromkeys(concepts, 0)

        difference = context.Attributes.supremum - concept.intent

        for atom in context.Attributes.fromint(difference).atoms():
            intersection = concept.extent & context.down(atom)

            subordinate = concept_index[intersection]
            counter[subordinate] += 1

            if (subordinate.intent.count() - concept.intent.count()) == counter[subordinate]:
                yield concept, subordinate


def _yield_edge_to_queue(concept_index, context, from_idx, to_idx, queue):
    for edge in _yield_edge(concept_index, context, from_idx, to_idx):
        queue.put(edge)

    queue.put(False)


def concept_cover(concepts, context):
    """
    Yields concepts and their subordinate concepts.

    Carpineto, Claudio, and Giovanni Romano. Concept data analysis: Theory and applications.
    John Wiley & Sons, 2004.
    """
    concept_index = dict(zip([int(concept.extent)
                              for concept in concepts], concepts))

    yield from _yield_edge(concept_index, context)


def concept_cover_parallel(concepts, context, n_of_workers):
    def split_indexes(a, n):
        k, m = divmod(len(a), n)
        return ((i * k + min(i, m), (i + 1) * k + min(i + 1, m)) for i in range(n))

    concept_index = dict(zip([int(concept.extent)
                              for concept in concepts], concepts))

    concept_chunks_idxs = tuple(
        split_indexes(concepts, n_of_workers))

    proces_queue_pairs = []

    for from_idx, to_idx in concept_chunks_idxs:
        queue = Queue()
        process = Process(target=_yield_edge_to_queue, args=(
            concept_index, context, from_idx, to_idx, queue))

        proces_queue_pairs.append((process, queue))

    for process, _ in proces_queue_pairs:
        process.start()

    n_of_finished_workers = 0

    concept_subordinate_pairs = []

    while n_of_finished_workers != n_of_workers:
        for process, queue in proces_queue_pairs:
            try:
                result = queue.get(block=False)

                if not result:
                    n_of_finished_workers += 1
                    break

                concept, subordinate = result
                concept_subordinate_pairs.append((concept, subordinate))
            except Empty:
                pass

    for process, _ in proces_queue_pairs:
        process.join()

    return concept_subordinate_pairs
