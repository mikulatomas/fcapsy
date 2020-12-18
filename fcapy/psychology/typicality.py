# Typicality implementation
#
# Rosch, Eleanor, and Carolyn B. Mervis. "Family resemblances: Studies in the internal structure of categories."
# Cognitive psychology 7.4 (1975): 573-605.
#
# Belohlavek, Radim, and Tomas Mikula. "Typicality in conceptual structures within the framework of formal concept analysis."

from itertools import compress
from fcapy.decorators import metadata
from fcapy.utils import iterator_mean
import math


def _calculate_similarities(item, items_to_compare, similarity_function):
    return map(lambda other: similarity_function(item, other), items_to_compare)


@metadata(name='Average Inner Typicality', short_name='Typ_avg')
def typicality_avg(item, items_to_compare, similarity_function):
    similarities = _calculate_similarities(
        item, items_to_compare, similarity_function)

    return iterator_mean(similarities)


@metadata(name='Minimal Inner Typicality', short_name='Typ_min')
def typicality_min(item, items_to_compare, similarity_function):
    similarities = _calculate_similarities(
        item, items_to_compare, similarity_function)

    return min(similarities)


def _calculate_weights(objects):
    objects = map(lambda x: x.bools(), objects)
    return [sum(y) for y in zip(*objects)]


@metadata(name='Rosch Inner Typicality', short_name='Typ_rosch')
def typicality_rosch(item, items_to_compare):
    weights = _calculate_weights(items_to_compare)

    return sum(compress(weights, item.bools()))


@metadata(name='Rosch Logarithm Inner Typicality', short_name='Typ_rosch_ln')
def typicality_rosch_ln(item, items_to_compare):
    weights = _calculate_weights(items_to_compare)
    weights = map(lambda x: math.log(x) if x != 0 else -math.inf, weights)

    return sum(compress(weights, item.bools()))
