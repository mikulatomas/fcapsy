"""Basic level

Belohlavek, Radim, and Trnecka, Martin.
Basic level of concepts in formal concept analysis 1: formalization and utilization.
International Journal of General Systems 49.7 (2020): 689-706.
"""

import typing
import statistics

import concepts.lattices

__all__ = ["basic_level_avg", "basic_level_min"]


def _theta_threshold(filtered_neighbors, neighbors, theta):
    return int((len(filtered_neighbors) / len(neighbors)) >= theta)


def _upper_cohesion_degree(
    concept, cohesion_degree, cohesion, similarity, theta, aggregation
):
    filtered_upper = tuple(
        filter(
            lambda neighbor: cohesion(neighbor, similarity) <= cohesion_degree,
            concept.upper_neighbors,
        )
    )

    if not filtered_upper:
        return 0.0

    threshold = _theta_threshold(filtered_upper, concept.upper_neighbors, theta)

    cohesion_ratio = map(
        lambda neighbor: cohesion(neighbor, similarity) / cohesion_degree,
        filtered_upper,
    )

    return (1 - aggregation(cohesion_ratio)) * threshold


def _lower_cohesion_degree(
    concept, cohesion_degree, cohesion, similarity, theta, aggregation
):
    filtered_lower = tuple(
        filter(
            lambda neighbor: cohesion(neighbor, similarity) >= cohesion_degree,
            concept.lower_neighbors,
        )
    )

    if not filtered_lower:
        return 0.0

    threshold = _theta_threshold(filtered_lower, concept.lower_neighbors, theta)

    cohesion_ratio = map(
        lambda neighbor: cohesion_degree / cohesion(neighbor, similarity),
        filtered_lower,
    )

    return aggregation(cohesion_ratio) * threshold


def _basic_level(
    concept: "concepts.lattices.Concept",
    cohesion: typing.Callable,
    similarity: typing.Callable,
    aggregation_upper: typing.Callable,
    aggregation_lower: typing.Callable,
    theta: typing.Optional[int] = 1,
) -> float:
    if (not concept.lower_neighbors) or (not concept.upper_neighbors):
        return 0.0

    # alpha 1
    cohesion_degree = cohesion(concept, similarity)

    if not cohesion_degree:
        return 0.0

    # alpha 2
    upper_cohesion_degree = _upper_cohesion_degree(
        concept, cohesion_degree, cohesion, similarity, theta, aggregation_upper
    )

    # alpha 3
    lower_cohesion_degree = _lower_cohesion_degree(
        concept, cohesion_degree, cohesion, similarity, theta, aggregation_lower
    )

    return cohesion_degree * upper_cohesion_degree * lower_cohesion_degree


def basic_level_avg(
    concept: "concepts.lattices.Concept",
    cohesion: typing.Callable,
    similarity: typing.Callable,
    theta: typing.Optional[int] = 1,
) -> float:
    """Calculate basic level of given concept based on average cohesion.

    For more details see:

    Belohlavek, Radim, and Trnecka, Martin.
    Basic level of concepts in formal concept analysis 1: formalization and utilization.
    International Journal of General Systems 49.7 (2020): 689-706.

    Args:
        concept (concepts.lattices.Concept)
        cohesion (typing.Callable)
        similarity (typing.Callable)
        theta (typing.Optional[int], optional): tuning parameter. Defaults to 1.

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> from fcapsy.cohesion import cohesion_avg
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> bl = [basic_level_avg(c, cohesion_avg, jaccard) for c in context.lattice]
        >>> context.lattice[bl.index(max(bl))]
        <Concept {sparrow, lark, chicken, vulture} <-> [2 legs flies] <=> flies>
        >>> max(bl) # doctest: +NUMBER
        0.108
    """

    return _basic_level(concept, cohesion, similarity, statistics.mean, statistics.mean, theta)


def basic_level_min(
    concept: "concepts.lattices.Concept",
    cohesion: typing.Callable,
    similarity: typing.Callable,
    theta: typing.Optional[int] = 1,
) -> float:
    """Calculate basic level of given concept based worst case (minimal) cohesion.

    For more details see:

    Belohlavek, Radim, and Trnecka, Martin.
    Basic level of concepts in formal concept analysis 1: formalization and utilization.
    International Journal of General Systems 49.7 (2020): 689-706.

    Args:
        concept (concepts.lattices.Concept)
        cohesion (typing.Callable)
        similarity (typing.Callable)
        theta (typing.Optional[int], optional): tuning parameter. Defaults to 1.

    Example:
        >>> from concepts import Context
        >>> from binsdpy.similarity import jaccard
        >>> from fcapsy.cohesion import cohesion_avg
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> bl = [basic_level_min(c, cohesion_avg, jaccard) for c in context.lattice]
        >>> context.lattice[bl.index(max(bl))]
        <Concept {sparrow, lark, chicken, vulture} <-> [2 legs flies] <=> flies>
        >>> max(bl) # doctest: +NUMBER
        0.108
    """

    return _basic_level(concept, cohesion, similarity, max, min, theta)
