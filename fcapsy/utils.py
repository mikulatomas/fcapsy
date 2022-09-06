import typing

import concepts
import concepts.lattices
import fcapsy.category


def get_context(
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"]
) -> "concepts.Context":
    """Simple function to return Context from given concept.

    Args:
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])

    Raises:
        ValueError: When concept type is not supported.

    Returns:
        concepts.Context: context
    """
    if isinstance(concept, fcapsy.category.Category):
        return concept.context
    elif isinstance(concept, concepts.lattices.Concept):
        return concept.lattice._context
    else:
        raise ValueError(
            "Only concepts.lattices.Concept or fcapsy.category.Category are supported."
        )


def get_vectors(
    concept: typing.Union["concepts.lattices.Concept", "fcapsy.category.Category"],
    item: str,
) -> typing.Dict:
    """Simple function to return tuple of binary vectors of extent/intent.

    Args:
        concept (typing.Union[concepts.lattices.Concept, fcapsy.category.Category])
        item (str)

    Returns:
        tuple: dict of vectors with item labels

    Example:
        >>> from concepts import Context
        >>> from fcapsy.category import Category
        >>> context = Context.fromstring('''
        ...          |2 legs |nests  |flies  |raptor |engine |
        ... sparrow  |   X   |   X   |   X   |       |       |
        ... lark     |   X   |   X   |   X   |       |       |
        ... penguin  |   X   |       |       |       |       |
        ... chicken  |   X   |   X   |   X   |       |       |
        ... vulture  |   X   |       |   X   |   X   |       |
        ... ''')
        >>> birds = context.lattice.supremum
        >>> get_vectors(birds, "lark")
        {'sparrow': Properties('11100'), 'lark': Properties('11100'), 'penguin': Properties('10000'), 'chicken': Properties('11100'), 'vulture': Properties('10110')}
        >>> category = Category(context, context._Objects.frommembers(["sparrow", "lark"]))
        >>> get_vectors(category, "lark")
        {'sparrow': Properties('11100'), 'lark': Properties('11100')}
        >>> get_vectors(birds, "nests")
        {'2 legs': Objects('11111')}
    """
    context = get_context(concept)

    if item in concept.extent:
        label_domain = context._intents
        items = concept.extent
        iter_set = concept._extent.iter_set()
    else:
        label_domain = context._extents
        items = concept.intent
        iter_set = concept._intent.iter_set()

    return dict(zip(items, map(label_domain.__getitem__, iter_set)))
