"""Typicality

Belohlavek, Radim, and Tomas Mikula.
Typicality: A formal concept analysis account.
International Journal of Approximate Reasoning (2021).

Belohlavek, Radim, and Mikula, Tomas.
Typicality in Conceptual Structures Within the Framework of Formal Concept Analysis.
Proceedings of CLA 2020 (2020): 33-45.
"""

import typing
import statistics

import concepts.lattices


__all__ = ["typicality_avg, typicality_min"]


def _get_vectors(concept, item):
    try:
        item_idx = concept.extent.index(item)
        label_domain = concept.lattice._context._intents
        vectors = tuple(map(label_domain.__getitem__, concept._extent.iter_set()))
    except ValueError:
        item_idx = concept.intent.index(item)
        label_domain = concept.lattice._context._extents
        vectors = tuple(map(label_domain.__getitem__, concept._intent.iter_set()))

    return vectors, vectors[item_idx]


def typicality_min(
    item: str, concept: "concepts.lattices.Concept", similarity: typing.Callable
) -> float:
    """Calculate typicality of object/attribute in given concept based on worst case (minimal) similarity.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)
        similarity (typing.Callable)

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> typicality_min('sparrow', birds, jaccard) # doctest: +NUMBER
        0.33
        >>> typicality_min('penguin', birds, jaccard) # doctest: +NUMBER
        0.33
    """

    vectors, item_vector = _get_vectors(concept, item)

    similarities = map(lambda v: similarity(v, item_vector), vectors)

    return min(similarities)


def typicality_avg(
    item: str, concept: "concepts.lattices.Concept", similarity: typing.Callable
) -> float:
    """Calculate typicality of object/attribute in given concept based on average similarity.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)
        similarity (typing.Callable)

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> typicality_avg('sparrow', birds, jaccard) # doctest: +NUMBER
        0.76
        >>> typicality_avg('penguin', birds, jaccard) # doctest: +NUMBER
        0.46
    """

    vectors, item_vector = _get_vectors(concept, item)

    similarities = map(lambda v: similarity(v, item_vector), vectors)

    return statistics.mean(similarities)
