# Typicality implementation
#
# Rosch, Eleanor, and Carolyn B. Mervis. "Family resemblances: Studies in the internal structure of categories."
# Cognitive psychology 7.4 (1975): 573-605.
#
# Belohlavek, Radim, and Tomas Mikula. "Typicality in conceptual structures within the framework of formal concept analysis."

from itertools import compress
import math


def _calculate_similarities(item, items_to_compare, similarity_function):
    return map(lambda other: similarity_function(item, other), items_to_compare)


@metadata(name='Average Inner Typicality', short_name='Typ_avg_in')
def typicality_avg(item, items_to_compare, similarity_function):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    similarities = _calculate_similarities(
        item, items_to_compare, similarity_function)

    return sum(similarities) / len(items_to_compare)


@metadata(name='Minimal Inner Typicality', short_name='Typ_min_in')
def typicality_min(item, items_to_compare, similarity_function):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    similarities = _calculate_similarities(
        item, items_to_compare, similarity_function)

    return min(similarities)


def _calculate_weights(objects):
    objects = map(lambda x: x.bools(), objects)
    return [sum(y) for y in zip(*objects)]


@metadata(name='Rosch Inner Typicality', short_name='Typ_rosch_in')
def typicality_rosch(item, items_to_compare):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    weights = _calculate_weights(items_to_compare)

    return sum(compress(weights, item.bools()))


@metadata(name='Rosch Logarithm Inner Typicality', short_name='Typ_rosch_in')
def typicality_rosch_ln(item, items_to_compare):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    weights = _calculate_weights(items_to_compare)
    weights = map(lambda x: math.log(x) if x != 0 else -math.inf, weights)

    return sum(compress(weights, item.bools()))


def contrast_typicality_avg(item, items_to_compare, similarity_function, contrast_items_to_compare):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    inner_typicality = typicality_avg(
        item, items_to_compare, similarity_function)

    outer_typicality = (typicality_avg(item, contrast_items, similarity_function)
                        for contrast_items in contrast_items_to_compare)
    outer_typicality = sum(outer_typicality) / len(outer_typicality)

    return inner_typicality * outer_typicality
