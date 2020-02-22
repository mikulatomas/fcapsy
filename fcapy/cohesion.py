from itertools import starmap
from itertools import combinations, combinations_with_replacement
from itertools import compress
from .decorators import info


@info('coh⋀')
def cohesion_min(concept, context, similarity_function, cache=None):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = context.filter_rows_by_extent(concept.extent)

    combs = combinations_with_replacement(concept_objects, 2)

    return min([similarity_function(x, y) for x, y in combs])


@info('coh⌀')
def cohesion_avg(concept, context, similarity_function, cache=None):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = context.filter_rows_by_extent(concept.extent)

    combs = combinations(concept_objects, 2)

    suma = sum([similarity_function(x, y) for x, y in combs])

    return suma / (len(concept.extent) * (len(concept.extent) - 1) / 2)
