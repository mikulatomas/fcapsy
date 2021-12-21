"""Concept cohesion

Belohlavek, Radim, and Martin Trnecka.
Basic level of concepts in formal concept analysis 1: formalization and utilization.
International Journal of General Systems 49.7 (2020): 689-706.
"""


import typing

import concepts.lattices

from itertools import combinations, starmap

__all__ = ["cohesion_min", "cohesion_avg"]


def cohesion_min(
    concept: "concepts.lattices.Concept", similarity: typing.Callable
) -> float:
    """Calculate cohesion of given concept as worst case (minimal) similarity of its objects.

    Example:
        >>> import concepts
        >>> from binsdpy import similarity
        >>> lattice = concepts.Context.fromstring(concepts.EXAMPLE).lattice
        >>> cohesion_min(lattice['+pl',], similarity.jaccard) # doctest: +NUMBER
        0.428
        >>> cohesion_min(lattice.atoms[0], similarity.jaccard)
        1.0
        >>> cohesion_min(lattice.infimum, similarity.jaccard)
        0
    """
    extent_size = len(concept.extent)

    if extent_size == 0:
        return 0
    elif extent_size == 1:
        return 1.0

    vectors = map(
        concept.lattice._context._intents.__getitem__, concept._extent.iter_set()
    )

    combs = combinations(vectors, 2)

    return min(starmap(similarity, combs))


def cohesion_avg(
    concept: "concepts.lattices.Concept", similarity: typing.Callable
) -> float:
    """Calculate cohesion of given concept as average similarity of its objects.

    Example:
        >>> import concepts
        >>> from binsdpy import similarity
        >>> lattice = concepts.Context.fromstring(concepts.EXAMPLE).lattice
        >>> cohesion_avg(lattice['+pl',], similarity.jaccard) # doctest: +NUMBER
        0.714
        >>> cohesion_avg(lattice.atoms[0], similarity.jaccard)
        1.0
        >>> cohesion_avg(lattice.infimum, similarity.jaccard)
        0

    """
    extent_size = len(concept.extent)

    if extent_size == 0:
        return 0
    elif extent_size == 1:
        return 1.0

    vectors = map(
        concept.lattice._context._intents.__getitem__, concept._extent.iter_set()
    )

    combs = combinations(vectors, 2)

    return (sum(starmap(similarity, combs)) + extent_size) / (
        extent_size * (extent_size + 1) / 2
    )
