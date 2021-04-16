from fcapsy import Context, Concept


def superordinate_concepts(context: Context, concept: Concept):
    """Calculates superordinate concepts of given concept in given context"""
    minimal = ~concept.extent

    for objects in context.Objects.atomic(minimal):
        new_intent = context.up(concept.extent | objects)
        new_extent = context.down(new_intent)

        if (new_extent & ~objects) & minimal:
            minimal &= ~objects
        else:
            yield Concept(new_extent, new_intent)


def subordinate_concepts(context: Context, concept: Concept):
    """Calculates subordinate concepts of given concept in given context"""
    minimal = ~concept.intent

    for attributes in context.Attributes.atomic(minimal):
        new_extent = context.down(concept.intent | attributes)
        new_intent = context.up(new_extent)

        if (new_intent & ~attributes) & minimal:
            minimal &= ~attributes
        else:
            yield Concept(new_extent, new_intent)
