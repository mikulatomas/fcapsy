from fcapy.cohesion import cohesion_min, cohesion_avg


def _degree(neighbors_filtered, neighbors):
    return int((len(neighbors_filtered) / len(neighbors)) >= 1)


def _alpha1(concept, context, cohesion_function, similarity_function, cache=None):
    return cohesion_function(concept, context, similarity_function, cache=cache)


def _alpha_helper(concept, context, neighbors, cohesion_function, similarity_function, cache=None):
    if len(neighbors) == 0:
        raise ValueError

    concept_cohesion = cohesion_function(
        concept, context, similarity_function, cache=cache)

    if concept_cohesion == 0:
        raise ValueError

    return concept_cohesion


def _alpha2_min(concept, context, upper_neighbors, cohesion_function, similarity_function, cache=None):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, upper_neighbors, cohesion_function, similarity_function, cache=cache)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function, cache=cache) <= concept_cohesion, upper_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    maximum = max(map(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function, cache=cache) / concept_cohesion, neighbors_filtered
    ))

    return (1 - maximum) * _degree(neighbors_filtered, upper_neighbors)


def _alpha2_avg(concept, context, upper_neighbors, cohesion_function, similarity_function, cache=None):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, upper_neighbors, cohesion_function, similarity_function, cache=cache)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function, cache=cache) <= concept_cohesion, upper_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    suma = sum(map(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function, cache=cache) / concept_cohesion, neighbors_filtered
    ))

    return (1 - (suma / len(neighbors_filtered))) * _degree(neighbors_filtered, upper_neighbors)


def _alpha3_min(concept, context, lower_neighbors, cohesion_function, similarity_function, cache=None):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, lower_neighbors, cohesion_function, similarity_function, cache=cache)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function, cache=cache) >= concept_cohesion, lower_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    minimum = min(map(lambda neighbor: concept_cohesion / cohesion_function(
        neighbor, context, similarity_function, cache=cache), neighbors_filtered
    ))

    return minimum * _degree(neighbors_filtered, lower_neighbors)


def _alpha3_avg(concept, context, lower_neighbors, cohesion_function, similarity_function, cache=None):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, lower_neighbors, cohesion_function, similarity_function, cache=cache)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function, cache=cache) >= concept_cohesion, lower_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    suma = sum(map(lambda neighbor: concept_cohesion / cohesion_function(
        neighbor, context, similarity_function, cache=cache), neighbors_filtered
    ))

    return (suma / len(neighbors_filtered)) * _degree(neighbors_filtered, lower_neighbors)


def basic_level_min(concept, context, upper_neighbors, lower_neighbors, cohesion_function, similarity_function, cache=None):
    alpha1 = _alpha1(concept, context, cohesion_function,
                     similarity_function, cache=cache)
    alpha2 = _alpha2_min(concept, context, upper_neighbors,
                         cohesion_function, similarity_function, cache=cache)
    alpha3 = _alpha3_min(concept, context, lower_neighbors,
                         cohesion_function, similarity_function, cache=cache)

    return alpha1 * alpha2 * alpha3


def basic_level_avg(concept, context, upper_neighbors, lower_neighbors, cohesion_function, similarity_function, cache=None):
    alpha1 = _alpha1(concept, context, cohesion_function,
                     similarity_function, cache=cache)
    alpha2 = _alpha2_avg(concept, context, upper_neighbors,
                         cohesion_function, similarity_function, cache=cache)
    alpha3 = _alpha3_avg(concept, context, lower_neighbors,
                         cohesion_function, similarity_function, cache=cache)

    return alpha1 * alpha2 * alpha3
