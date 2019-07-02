from itertools import starmap
from itertools import combinations, combinations_with_replacement
from itertools import compress


def cohesion_min(concept, context, similarity_function):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = compress(context.rows, concept.extent.bools())

    combs = combinations_with_replacement(concept_objects, 2)

    return min(starmap(similarity_function, combs))


def cohesion_avg(concept, context, similarity_function):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = compress(context.rows, concept.extent.bools())

    combs = combinations(concept_objects, 2)

    suma = sum(starmap(similarity_function, combs))

    return suma / (len(concept.extent) * (len(concept.extent) - 1) / 2)
