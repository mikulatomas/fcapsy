from itertools import starmap
from itertools import combinations, combinations_with_replacement
from itertools import compress


def cohesion_min(concept, context, similarity_function, cache=None):
    if cache is not None:
        concept_id = 'c' + str(int(concept.intent))
        cached_cohesion = cache.get(concept_id)

        if cached_cohesion is not None:
            return cached_cohesion

    if len(concept.extent) == 0:
        if cache is not None:
            cache[concept_id] = 0
        return 0

    if len(concept.extent) == 1:
        if cache is not None:
            cache[concept_id] = 1
        return 1

    concept_objects = compress(context.rows, concept.extent.bools())

    combs = combinations_with_replacement(concept_objects, 2)

    # result = min(starmap(similarity_function, combs))
    result = min([similarity_function(x, y, cache=cache) for x, y in combs])

    if cache is not None:
        cache[concept_id] = result

    return result


def cohesion_avg(concept, context, similarity_function, cache=None):
    if len(concept.extent) == 0:
        return 0

    if len(concept.extent) == 1:
        return 1

    concept_objects = compress(context.rows, concept.extent.bools())

    combs = combinations(concept_objects, 2)

    # suma = sum(starmap(similarity_function, combs))
    suma = sum([similarity_function(x, y, cache=cache) for x, y in combs])

    return suma / (len(concept.extent) * (len(concept.extent) - 1) / 2)
