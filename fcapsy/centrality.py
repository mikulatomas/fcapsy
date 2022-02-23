__all__ = ["centrality"]


def centrality(item: str, concept: "concepts.lattices.Concept") -> float:
    """Calculates centrality of object/attribute in the given concept.
    The object/attribute does not has to be from the extent/intent.

    Args:
        item (str): object or attribute name
        concept (concepts.lattices.Concept)

    Returns:
        float: centrality

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
        >>> centrality("raptor", birds)
        0.2
        >>> centrality("flies", birds)
        0.8
        >>> centrality("2 legs", birds)
        1.0
    """
    context = concept.lattice._context

    try:
        instances_with_item = context.intension([item], raw=True)
        Vector = type(concept._intent)
        concept_core = concept._intent
    except KeyError:
        instances_with_item = context.extension([item], raw=True)
        Vector = type(concept._extent)
        concept_core = concept._extent

    occurence_in_concept = Vector.fromint(instances_with_item & concept_core).count()

    if not instances_with_item.count():
        return 0.0

    return (occurence_in_concept / instances_with_item.count()) * (
        occurence_in_concept / concept._extent.count()
    )
