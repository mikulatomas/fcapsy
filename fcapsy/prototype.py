import typing

import concepts.lattices
import fcapsy.category
import numpy as np

from .utils import get_vectors


def prototype(
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
) -> np.ndarray:
    """Calcualtes prototype of given concept.

    Args:
        concept (typing.Union[&quot;concepts.lattices.Concept&quot;, &quot;fcapsy.category.Category&quot;]): concept

    Returns:
        np.ndarray: prototype

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
        >>> prototype(birds)
        array([1. , 0.6, 0.8, 0.2, 0. ])
    """
    vectors = get_vectors(concept, concept.extent[0]).values()

    return np.array([a.bools() for a in vectors]).astype(int).mean(axis=0)
