from fcapy import Context, Concept


def upper_neighbors(context: Context, concept: Concept):
    """Calculates upper neighbors of given concept in given context"""
    minimal = ~concept.extent

    for objects in context._Objects.atomic(minimal):
        new_intent = context.up(concept.extent | objects)
        new_extent = context.down(new_intent)

        if (new_extent & ~objects) & minimal:
            minimal &= ~objects
        else:
            yield Concept(new_extent, new_intent)


def lower_neighbors(context: Context, concept: Concept):
    """Calculates lower neighbors of given concept in given context"""
    minimal = ~concept.intent

    for attributes in context._Attributes.atomic(minimal):
        new_extent = context.down(concept.intent | attributes)
        new_intent = context.up(new_extent)

        if (new_intent & ~attributes) & minimal:
            minimal &= ~attributes
        else:
            yield Concept(new_extent, new_intent)
