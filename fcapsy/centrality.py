__all__ = ["centrality"]


# def attribute_centrality(attribute: str, concept: "concepts.lattices.Concept") -> float:
#     context = concept.lattice._context
#     objects_with_attribute = context.extension([attribute], raw=True).bools()

#     return sum(
#         [int(objects_with_attribute[idx]) for idx in concept._extent.iter_set()]
#     ) / len(concept.extent)


# def intent_centrality(attribute: str, concept: "concepts.lattices.Concept") -> float:
#     context = concept.lattice._context
#     objects_with_attribute = context.extension([attribute], raw=True).members()

#     return len(concept.extent) / len(objects_with_attribute)


# def attribute_centrality(attribute: str, concept: "concepts.lattices.Concept") -> float:
#     context = concept.lattice._context
#     objects_with_attribute = context.extension([attribute], raw=True)

#     occurence_in_concept = context._Objects.fromint(
#         objects_with_attribute & concept._extent
#     ).count()

#     if not objects_with_attribute.count():
#         return float(0)

#     return (occurence_in_concept / objects_with_attribute.count()) * (
#         occurence_in_concept / concept._extent.count()
#     )


# def object_centrality(object: str, concept: "concepts.lattices.Concept") -> float:
#     context = concept.lattice._context
#     attributes_with_object = context.intension([object], raw=True)

#     occurence_in_concept = context._Properties.fromint(
#         attributes_with_object & concept._intent
#     ).count()

#     if not attributes_with_object.count():
#         return float(0)

#     return (occurence_in_concept / attributes_with_object.count()) * (
#         occurence_in_concept / concept._extent.count()
#     )


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
