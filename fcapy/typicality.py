from itertools import starmap
from itertools import combinations_with_replacement
from itertools import compress


# def _find_zero_attributes(objects):
#     result = objects[0]

#     for row in objects[1:]:
#         result |= row

#     return objects[0].fromint(result).complement()


def _find_zero_items(items):
    if not items:
        return 0

    result = items[0]

    for row in items[1:]:
        result |= row

    return items[0].fromint(result).complement()


def _typicality_helper(concept, context, definitions_items, remove_zeros, remove_definition_items, mode):
    if mode is 'objects':
        items = list(compress(context.rows, definitions_items.bools()))
        universum_object = context._Attributes

    elif mode is 'attributes':
        items = list(compress(context.columns, definitions_items.bools()))
        universum_object = context._Objects

    items_to_remove = universum_object.infimum

    if remove_zeros:
        items_to_remove |= _find_zero_items(items)
        items_to_remove = universum_object.fromint(
            items_to_remove)

    if remove_definition_items:
        items_to_remove |= definitions_items
        items_to_remove = universum_object.fromint(
            items_to_remove)

    return items, items_to_remove


def typicality_avg(item, concept, context, definitions_items, similarity_function, remove_zeros=False, remove_definition_items=False, mode='objects'):
    """
    Calculates average typicality for given item (object or attribute).

    Parameters:
    item: one item, object or attribute
    concept: concept in which typicality is calculated
    context: context in which concept exists
    similarity_function: similarity functions used for typicality calculation
    remove_zeros (bool): if zeroes should be removed from universum
    remove_definition_items (bool): if definition items (extent or intent) should be removed
    mode ('objects' or 'attributes') if objects or attributes are used for typicality calculation

    Returns:
    float: typicality of given item

   """
    items, items_to_remove = _typicality_helper(concept, context, definitions_items, remove_zeros,
                                                remove_definition_items, mode)

    if not items:
        return 0

    suma = sum(map(lambda x: similarity_function(
        item, x, items_to_remove), items))

    return suma / len(definitions_items)


def typicality_min(item, concept, context, definitions_items, similarity_function, remove_zeros=False, remove_definition_items=False, mode='objects'):
    """
    Calculates minimal typicality for given item (object or attribute).

    Parameters:
    item: one item, object or attribute
    concept: concept in which typicality is calculated
    context: context in which concept exists
    similarity_function: similarity functions used for typicality calculation
    remove_zeros (bool): if zeroes should be removed from universum
    remove_definition_items (bool): if definition items (extent or intent) should be removed
    mode ('objects' or 'attributes') if objects or attributes are used for typicality calculation

    Returns:
    float: typicality of given item

   """

    items, items_to_remove = _typicality_helper(concept, context, definitions_items, remove_zeros,
                                                remove_definition_items, mode)

    if not items:
        return 0

    minimum = min(map(lambda x: similarity_function(
        item, x, items_to_remove), items))

    return minimum


# def typicality_avg(obj, concept, context, similarity_function, remove_zeros=False, remove_intent=False):
#     concept_objects = list(compress(context.rows, concept.extent.bools()))

#     attributes_to_remove = context._Attributes.infimum

#     if remove_zeros:
#         attributes_to_remove |= _find_zero_attributes(concept_objects)
#         attributes_to_remove = context._Attributes.fromint(
#             attributes_to_remove)

#     if remove_intent:
#         attributes_to_remove |= concept.intent
#         attributes_to_remove = context._Attributes.fromint(
#             attributes_to_remove)

#     suma = sum(map(lambda x: similarity_function(
#         obj, x, attributes_to_remove), concept_objects))

#     return suma / len(concept.extent)


# def typicality_min(obj, concept, context, similarity_function, remove_zeros=False, remove_intent=False):
#     concept_objects = list(compress(context.rows, concept.extent.bools()))

#     attributes_to_remove = context._Attributes.infimum

#     if remove_zeros:
#         attributes_to_remove |= _find_zero_attributes(concept_objects)
#         attributes_to_remove = context._Attributes.fromint(
#             attributes_to_remove)

#     if remove_intent:
#         attributes_to_remove |= concept.intent
#         attributes_to_remove = context._Attributes.fromint(
#             attributes_to_remove)

#     minimum = min(
#         map(lambda x: similarity_function(obj, x, attributes_to_remove), concept_objects))

#     return minimum


def _calculate_weights(objects):
    objects = map(lambda x: x.bools(), objects)
    return [sum(y) for y in zip(*objects)]


def typicality_rosch(obj, concept, context):
    concept_objects = list(compress(context.rows, concept.extent.bools()))

    weights = _calculate_weights(concept_objects)

    return sum(compress(weights, obj.bools()))
