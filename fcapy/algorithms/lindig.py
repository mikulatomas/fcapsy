from fcapy import Context, Concept


def upper_neighbors(context: Context, concept: Concept):
    """Calculates upper neighbors of given concept in given context"""
    minimal = ~concept.extent

    for objects in context._Objects.atomic(minimal):
        new_intent = context.up(concept.extent | objects)
        new_extent = context.down(new_intent)

        if minimal & (new_extent & ~objects):
            minimal &= ~objects
        else:
            neighbor = Concept(
                context._Objects.fromint(new_extent),
                context._Attributes.fromint(new_intent))

            yield neighbor


def lower_neighbors(context: Context, concept: Concept):
    """Calculates lower neighbors of given concept in given context"""
    minimal = ~concept.intent

    for attributes in context._Attributes.atomic(minimal):
        new_extent = context.down(concept.intent | attributes)
        new_intent = context.up(new_extent)

        if minimal & (new_intent & ~attributes):
            minimal &= ~attributes
        else:
            neighbor = Concept(
                context._Objects.fromint(new_extent),
                context._Attributes.fromint(new_intent))

            yield neighbor
