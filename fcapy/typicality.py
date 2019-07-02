from itertools import starmap
from itertools import combinations_with_replacement
from itertools import compress


def _find_zero_attributes(objects):
    result = objects[0]

    for row in objects[1:]:
        result |= row

    return objects[0].fromint(result).complement()


def typicality_avg(obj, concept, context, similarity_function, remove_zeros=False, remove_intent=False):
    concept_objects = list(compress(context.rows, concept.extent.bools()))

    attributes_to_remove = context._Attributes.infimum

    if remove_zeros:
        attributes_to_remove |= _find_zero_attributes(concept_objects)
        attributes_to_remove = context._Attributes.fromint(
            attributes_to_remove)

    if remove_intent:
        attributes_to_remove |= concept.intent
        attributes_to_remove = context._Attributes.fromint(
            attributes_to_remove)

    suma = sum(map(lambda x: similarity_function(
        obj, x, attributes_to_remove), concept_objects))

    return suma / len(concept.extent)


def typicality_min(obj, concept, context, similarity_function, remove_zeros=False, remove_intent=False):
    concept_objects = list(compress(context.rows, concept.extent.bools()))

    attributes_to_remove = context._Attributes.infimum

    if remove_zeros:
        attributes_to_remove |= _find_zero_attributes(concept_objects)
        attributes_to_remove = context._Attributes.fromint(
            attributes_to_remove)

    if remove_intent:
        attributes_to_remove |= concept.intent
        attributes_to_remove = context._Attributes.fromint(
            attributes_to_remove)

    minimum = min(
        map(lambda x: similarity_function(obj, x, attributes_to_remove), concept_objects))

    return minimum


def _calculate_weights(objects):
    objects = map(lambda x: x.bools(), objects)
    return [sum(y) for y in zip(*objects)]


def typicality_rosch(obj, concept, context):
    concept_objects = list(compress(context.rows, concept.extent.bools()))

    weights = _calculate_weights(concept_objects)

    return sum(compress(weights, obj.bools()))
