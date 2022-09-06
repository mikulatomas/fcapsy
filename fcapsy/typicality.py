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
import fcapsy.category

from .item_weights import characteristic, absence, presence
from .utils import get_vectors


def typicality_similarity(
    item: str,
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
    similarity: typing.Callable,
    aggregate_function: typing.Callable = statistics.mean,
    empty_attributes: bool = True,
) -> float:
    """Calculate typicality of object/attribute in given concept based on similarity.

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])
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
    vectors = get_vectors(concept, item)
    item_property_vector = vectors[item]
    mask = None

    if not empty_attributes:
        mask = reduce(operator.or_, vectors.values())

    similarities = map(
        lambda v: similarity(v, item_property_vector, mask), vectors.values()
    )

    return aggregate_function(similarities)


def typicality_weights(
    item: str,
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
    a: float,
    b: float,
) -> float:
    """Calculates typicality based on attribute/object weights.

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])

    Returns:
        float: typicality
    """
    vectors = get_vectors(concept, item)
    item_property_vector = vectors[item]

    Vector = type(item_property_vector)

    item_property_vector_complement = Vector.fromint(
        Vector.supremum ^ item_property_vector
    )

    weights_presence = (
        presence(item_property, concept)
        for item_property in item_property_vector.members()
    )

    weights_absence = (
        absence(item_property, concept)
        for item_property in item_property_vector_complement.members()
    )

    return a * sum(weights_presence) + b * sum(weights_absence)


def typicality_characteristic(
    item: str,
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
    characteristic_function: typing.Callable = characteristic,
) -> float:
    """Calculates typicality based on attribute/object characteristic.

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])

    Returns:
        float: typicality
    """
    vectors = get_vectors(concept, item)
    item_property_vector = vectors[item]

    characteristics = (
        characteristic_function(item_property, concept)
        for item_property in item_property_vector.members()
    )

    return sum(characteristics)


def typicality_min(
    item: str,
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
    similarity: typing.Callable,
    empty_attributes: bool = True,
) -> float:
    """Calculate typicality of object/attribute in given concept based on worst case (minimal) similarity.

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])
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
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
    similarity: typing.Callable,
    empty_attributes: bool = True,
) -> float:
    """Calculate typicality of object/attribute in given concept based on average similarity.

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])
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
