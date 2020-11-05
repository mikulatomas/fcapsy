# Cohesion implementation
#
# Belohlavek, Radim, and Martin Trnecka. "Basic level in formal concept analysis: Interesting concepts and psychological ramifications."
# Twenty-Third International Joint Conference on Artificial Intelligence. 2013.
#
# Belohlavek, Radim, and Martin Trnecka. "Basic level of concepts in formal concept analysis."
# International Conference on Formal Concept Analysis. Springer, Berlin, Heidelberg, 2012.

from itertools import combinations, combinations_with_replacement
from fcapy.decorators import metadata


@metadata(name='Minimal Concept Cohesion', short_name='Coh_m')
def cohesion_min(concept, context, similarity_function, cache=None):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = context.filter_rows_by_extent(concept.extent)

    combs = combinations_with_replacement(concept_objects, 2)

    return min([similarity_function(x, y) for x, y in combs])


@metadata(name='Average Concept Cohesion', short_name='Coh_avg')
def cohesion_avg(concept, context, similarity_function, cache=None):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = context.filter_rows_by_extent(concept.extent)

    combs = combinations(concept_objects, 2)

    suma = sum([similarity_function(x, y) for x, y in combs])

    return suma / (len(concept.extent) * (len(concept.extent) - 1) / 2)
