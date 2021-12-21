__all__ = ["centrality"]


def centrality(item: str, concept: "concepts.lattices.Concept") -> float:
    context = concept.lattice._context

    try:
        instances_with_item = context.intension([item], raw=True)
        Vector = context._Properties
        concept_core = concept._intent
    except KeyError:
        instances_with_item = context.extension([item], raw=True)
        Vector = context._Objects
        concept_core = concept._extent

    occurence_in_concept = Vector.fromint(instances_with_item & concept_core).count()

    if not instances_with_item.count():
        return 0.0

    return (occurence_in_concept / instances_with_item.count()) * (
        occurence_in_concept / concept._extent.count()
    )
