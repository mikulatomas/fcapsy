# Typicality implementation
#
# Rosch, Eleanor, and Carolyn B. Mervis. "Family resemblances: Studies in the internal structure of categories."
# Cognitive psychology 7.4 (1975): 573-605.

from itertools import starmap
from itertools import combinations_with_replacement
from itertools import compress
from .decorators import info
import math


# def _find_zero_items(items):
#     if not items:
#         return 0

#     result = items[0]

#     for row in items[1:]:
#         result |= row

#     return items[0].fromint(result).complement()


def _calculate_similarities(item, items_to_compare, similarity_function):
    return map(lambda other: similarity_function(item, other), items_to_compare)


@info('Typ⌀')
def typicality_avg(item, items_to_compare, similarity_function):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    similarities = _calculate_similarities(
        item, items_to_compare, similarity_function)

    return sum(similarities) / len(items_to_compare)


@info('Typ⋀')
def typicality_min(item, items_to_compare, similarity_function):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    similarities = _calculate_similarities(
        item, items_to_compare, similarity_function)

    return min(similarities)


def _calculate_weights(objects):
    objects = map(lambda x: x.bools(), objects)
    return [sum(y) for y in zip(*objects)]


@info('Rosch')
def typicality_rosch(item, items_to_compare):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    weights = _calculate_weights(items_to_compare)

    return sum(compress(weights, item.bools()))


@info('Rosch ln')
def typicality_rosch_ln(item, items_to_compare):
    if type(item) is not type(items_to_compare[0]):
        raise ValueError("Wrong type of items!")

    weights = _calculate_weights(items_to_compare)
    weights = map(lambda x: math.log(x) if x != 0 else -math.inf, weights)

    return sum(compress(weights, item.bools()))
