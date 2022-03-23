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
import operator
from functools import reduce

import concepts.lattices

from .centrality import centrality


__all__ = [
    "typicality_similarity",
    "typicality_avg",
    "typicality_min",
    "typicality_centrality",
]


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


def typicality_similarity(
    item: str,
    concept: "concepts.lattices.Concept",
    similarity: typing.Callable,
    aggregate_function: typing.Callable = statistics.mean,
    empty_attributes: bool = True,
) -> float:
    """Calculate typicality of object/attribute in given concept based on similarity.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)
        similarity (typing.Callable)
        aggregate_function (typing.Callable): aggregate function used for aggregate similarity values
        empty_attributes (bool): if empty attributes (zeros columns) should be included

    Returns:
        float: typicality

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |engine |
        ... sparrow  |   X   |   X   |   X   |       |       |
        ... lark     |   X   |   X   |   X   |       |       |
        ... penguin  |   X   |       |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |       |
        ... vulture  |   X   |       |   X   |   X   |       |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> typicality_similarity("sparrow", birds, jaccard) # doctest: +NUMBER
        0.76
        >>> typicality_similarity("penguin", birds, jaccard) # doctest: +NUMBER
        0.46
        >>> from binsdpy.similarity import smc
        >>> typicality_similarity("penguin", birds, smc, empty_attributes=False) # doctest: +NUMBER
        0.5
    """
    vectors, item_vector = _get_vectors(concept, item)
    mask = None

    if not empty_attributes:
        mask = reduce(operator.or_, vectors)

    similarities = map(lambda v: similarity(v, item_vector, mask), vectors)

    return aggregate_function(similarities)


def typicality_centrality(
    item: str,
    concept: "concepts.lattices.Concept",
    aggregate_function: typing.Callable = statistics.mean,
) -> float:
    """Calculates typicality based on attribute/object centrality.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)
        average (bool): flag if centrality should be averaged

    Returns:
        float: typicality
    """
    _, item_vector = _get_vectors(concept, item)

    centralities = (centrality(item, concept) for item in item_vector.members())

    return aggregate_function(centralities)


def typicality_min(
    item: str,
    concept: "concepts.lattices.Concept",
    similarity: typing.Callable,
    empty_attributes: bool = True,
) -> float:
    """Calculate typicality of object/attribute in given concept based on worst case (minimal) similarity.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)
        similarity (typing.Callable)
        empty_attributes (bool): if empty attributes (zeros columns) should be included

    Returns:
        float: typicality

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |engine |
        ... sparrow  |   X   |   X   |   X   |       |       |
        ... lark     |   X   |   X   |   X   |       |       |
        ... penguin  |   X   |       |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |       |
        ... vulture  |   X   |       |   X   |   X   |       |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> typicality_min("sparrow", birds, jaccard) # doctest: +NUMBER
        0.33
        >>> typicality_min("penguin", birds, jaccard) # doctest: +NUMBER
        0.33
        >>> from binsdpy.similarity import smc
        >>> typicality_min("penguin", birds, smc, empty_attributes=False) # doctest: +NUMBER
        0.5
    """
    return typicality_similarity(item, concept, similarity, min, empty_attributes)


def typicality_avg(
    item: str,
    concept: "concepts.lattices.Concept",
    similarity: typing.Callable,
    empty_attributes: bool = True,
) -> float:
    """Calculate typicality of object/attribute in given concept based on average similarity.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)
        similarity (typing.Callable)
        empty_attributes (bool): if empty attributes (zeros columns) should be included

    Returns:
        float: typicality

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |engine |
        ... sparrow  |   X   |   X   |   X   |       |       |
        ... lark     |   X   |   X   |   X   |       |       |
        ... penguin  |   X   |       |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |       |
        ... vulture  |   X   |       |   X   |   X   |       |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> typicality_avg("sparrow", birds, jaccard) # doctest: +NUMBER
        0.76
        >>> typicality_avg("penguin", birds, jaccard) # doctest: +NUMBER
        0.46
        >>> from binsdpy.similarity import smc
        >>> typicality_avg("penguin", birds, smc, empty_attributes=False) # doctest: +NUMBER
        0.5
    """
    return typicality_similarity(
        item, concept, similarity, statistics.mean, empty_attributes
    )
