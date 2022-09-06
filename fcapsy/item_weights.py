import typing

import concepts.lattices
import fcapsy.category

from .utils import get_context


__all__ = ["presence", "absence", "characteristic", "characteristic_r"]


def _get_vectors(item, concept):
    context = get_context(concept)

    try:
        instances_with_item = context.intension([item], raw=True)
        Vector = type(concept._intent)
        universum = Vector.supremum
        concept_core = concept._intent
    except KeyError:
        instances_with_item = context.extension([item], raw=True)
        Vector = type(concept._extent)
        universum = Vector.supremum
        concept_core = concept._extent

    return instances_with_item, concept_core, Vector, universum


def presence(
    item, concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"]
):
    """_summary_

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])

    Returns:
        _type_: _description_

    Example:
        >>> from concepts import Context
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> presence("2 legs", birds)
        5
        >>> presence("nests", birds)
        3
        >>> flies = birds.lower_neighbors[0]
        >>> presence("2 legs", flies)
        4
    """
    instances_with_item, concept_core, Vector, _ = _get_vectors(item, concept)

    occurence_in_concept = Vector.fromint(instances_with_item & concept_core).count()

    return occurence_in_concept


def absence(
    item, concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"]
):
    """_summary_

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])

    Returns:
        _type_: _description_

    Example:
        >>> from concepts import Context
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> absence("2 legs", birds)
        0
        >>> absence("nests", birds)
        2
        >>> flies = birds.lower_neighbors[0]
        >>> absence("raptor", flies)
        3
    """
    instances_with_item, concept_core, Vector, universum = _get_vectors(item, concept)

    absence_in_concept = Vector.fromint(
        (universum ^ instances_with_item) & concept_core
    ).count()

    return absence_in_concept


def characteristic(
    item: str,
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
) -> float:
    """Calculates characteristic of object/attribute in the given concept.
    The object/attribute does not has to be from the extent/intent.

    Args:
        item (str): object or attribute name
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])

    Returns:
        float: characteristic

    Example:
        >>> from concepts import Context
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |
        ... sparrow  |   X   |   X   |   X   |       |
        ... lark     |   X   |   X   |   X   |       |
        ... penguin  |   X   |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |
        ... vulture  |   X   |       |   X   |   X   |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> birds.extent
        ('sparrow', 'lark', 'penguin', 'chicken', 'vulture')
        >>> characteristic("raptor", birds)
        0.2
        >>> characteristic("flies", birds)
        0.8
        >>> characteristic("2 legs", birds)
        1.0
    """
    instances_with_item, concept_core, Vector, _ = _get_vectors(item, concept)

    occurence_in_concept = Vector.fromint(instances_with_item & concept_core).count()

    if not instances_with_item.count():
        return 0.0

    return (occurence_in_concept / instances_with_item.count()) * (
        occurence_in_concept / concept_core.count()
    )


def characteristic_r(
    item: str,
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
) -> float:
    instances_with_item, concept_core, Vector, _ = _get_vectors(item, concept)

    occurence_in_concept = Vector.fromint(instances_with_item & concept_core).count()

    if not instances_with_item.count():
        return 0.0

    universum = Vector.supremum
    universum_minus_core = Vector.fromint(universum & (universum ^ concept_core))
    universum_minus_core_minus_instances_with_item = Vector.fromint(
        universum_minus_core & (universum ^ instances_with_item)
    )

    return (occurence_in_concept / concept_core.count()) * (
        universum_minus_core_minus_instances_with_item.count()
        / universum_minus_core.count()
    )
