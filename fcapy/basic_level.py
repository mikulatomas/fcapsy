from .cohesion import cohesion_min, cohesion_avg
from .decorators import info


def _degree(neighbors_filtered, neighbors):
    return int((len(neighbors_filtered) / len(neighbors)) >= 1)


def _alpha1(concept, context, cohesion_function, similarity_function):
    return cohesion_function(concept, context, similarity_function)


def _alpha_helper(concept, context, neighbors, cohesion_function, similarity_function):
    if len(neighbors) == 0:
        raise ValueError

    concept_cohesion = cohesion_function(
        concept, context, similarity_function)

    if concept_cohesion == 0:
        raise ValueError

    return concept_cohesion


def _alpha2_min(concept, context, upper_neighbors, cohesion_function, similarity_function):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, upper_neighbors, cohesion_function, similarity_function)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) <= concept_cohesion, upper_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    maximum = max(map(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) / concept_cohesion, neighbors_filtered
    ))

    return (1 - maximum) * _degree(neighbors_filtered, upper_neighbors)


def _alpha2_avg(concept, context, upper_neighbors, cohesion_function, similarity_function):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, upper_neighbors, cohesion_function, similarity_function)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) <= concept_cohesion, upper_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    suma = sum(map(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) / concept_cohesion, neighbors_filtered
    ))

    return (1 - (suma / len(neighbors_filtered))) * _degree(neighbors_filtered, upper_neighbors)


def _alpha3_min(concept, context, lower_neighbors, cohesion_function, similarity_function):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, lower_neighbors, cohesion_function, similarity_function)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) >= concept_cohesion, lower_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    minimum = min(map(lambda neighbor: concept_cohesion / cohesion_function(
        neighbor, context, similarity_function), neighbors_filtered
    ))

    return minimum * _degree(neighbors_filtered, lower_neighbors)


def _alpha3_avg(concept, context, lower_neighbors, cohesion_function, similarity_function):
    try:
        concept_cohesion = _alpha_helper(
            concept, context, lower_neighbors, cohesion_function, similarity_function)
    except ValueError:
        return 0

    neighbors_filtered = list(filter(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) >= concept_cohesion, lower_neighbors))

    if len(neighbors_filtered) == 0:
        return 0

    suma = sum(map(lambda neighbor: concept_cohesion / cohesion_function(
        neighbor, context, similarity_function), neighbors_filtered
    ))

    return (suma / len(neighbors_filtered)) * _degree(neighbors_filtered, lower_neighbors)


@info('BL⋀')
def basic_level_min(concept, context, upper_neighbors, lower_neighbors, cohesion_function, similarity_function):
    alpha1 = _alpha1(concept, context, cohesion_function,
                     similarity_function)
    alpha2 = _alpha2_min(concept, context, upper_neighbors,
                         cohesion_function, similarity_function)
    alpha3 = _alpha3_min(concept, context, lower_neighbors,
                         cohesion_function, similarity_function)

    return alpha1 * alpha2 * alpha3


@info('BL⌀')
def basic_level_avg(concept, context, upper_neighbors, lower_neighbors, cohesion_function, similarity_function):
    alpha1 = _alpha1(concept, context, cohesion_function,
                     similarity_function)
    alpha2 = _alpha2_avg(concept, context, upper_neighbors,
                         cohesion_function, similarity_function)
    alpha3 = _alpha3_avg(concept, context, lower_neighbors,
                         cohesion_function, similarity_function)

    return alpha1 * alpha2 * alpha3
