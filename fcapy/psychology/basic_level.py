# Basic level implementation
#
# Belohlavek, Radim, and Martin Trnecka.
# "Basic level in formal concept analysis: Interesting concepts and psychological ramifications."
# Twenty-Third International Joint Conference on Artificial Intelligence. 2013.
#
# Belohlavek, Radim, and Martin Trnecka.
# "Basic level of concepts in formal concept analysis."
# International Conference on Formal Concept Analysis. Springer, Berlin, Heidelberg, 2012.

# Constant θ is fixed to 1

import operator

from fcapy.decorators import metadata
from fcapy.utils import iterator_mean


def _degree(neighbors_filtered, neighbors):
    return int((len(neighbors_filtered) / len(neighbors)) >= 1)


def _calculate_concept_cohesion(concept, context, neighbors,
                                cohesion_function, similarity_function):
    if not neighbors:
        raise ValueError

    concept_cohesion = cohesion_function(
        concept, context, similarity_function)

    if concept_cohesion == 0:
        raise ValueError

    return concept_cohesion


def _filter_neighbors(cohesion_function, context, similarity_function,
                      concept_cohesion, neighbors, comparation):
    return tuple(filter(lambda neighbor: comparation(cohesion_function(
        neighbor, context, similarity_function), concept_cohesion), neighbors))


def _alpha1(concept, context, cohesion_function, similarity_function):
    return cohesion_function(concept, context, similarity_function)


def _alpha2(concept, context, upper_neighbors,
            cohesion_function, similarity_function, variant='avg'):
    try:
        concept_cohesion = _calculate_concept_cohesion(
            concept, context, upper_neighbors, cohesion_function, similarity_function)
    except ValueError:
        return 0

    neighbors_filtered = _filter_neighbors(
        cohesion_function, context, similarity_function,
        concept_cohesion, upper_neighbors, operator.le)

    # Prevents division by zero
    if not neighbors_filtered:
        return 0

    cohesion_ratio = map(lambda neighbor: cohesion_function(
        neighbor, context, similarity_function) / concept_cohesion, neighbors_filtered)

    if variant == 'avg':
        intermediate_result = iterator_mean(cohesion_ratio)
    else:
        intermediate_result = max(cohesion_ratio)

    return (1 - intermediate_result) * _degree(neighbors_filtered, upper_neighbors)


def _alpha3(concept, context, lower_neighbors,
            cohesion_function, similarity_function, variant='avg'):
    try:
        concept_cohesion = _calculate_concept_cohesion(
            concept, context, lower_neighbors, cohesion_function, similarity_function)
    except ValueError:
        return 0

    neighbors_filtered = _filter_neighbors(
        cohesion_function, context, similarity_function,
        concept_cohesion, lower_neighbors, operator.ge)

    # Prevents division by zero
    if not neighbors_filtered:
        return 0

    cohesion_ratio = map(lambda neighbor: concept_cohesion / cohesion_function(
        neighbor, context, similarity_function), neighbors_filtered)

    if variant == 'avg':
        intermediate_result = iterator_mean(cohesion_ratio)
    else:
        intermediate_result = min(cohesion_ratio)

    return intermediate_result * _degree(neighbors_filtered, lower_neighbors)


def _bl_helper(concept, context, upper_neighbors, lower_neighbors,
               cohesion_function, similarity_function, variant):
    alpha1 = _alpha1(concept, context, cohesion_function,
                     similarity_function)
    alpha2 = _alpha2(concept, context, upper_neighbors,
                     cohesion_function, similarity_function, variant)
    alpha3 = _alpha3(concept, context, lower_neighbors,
                     cohesion_function, similarity_function, variant)

    return alpha1 * alpha2 * alpha3


@metadata(name='Minimal Basic Level', short_name='BL_min', latex='BL_\\mathrm{min}')
def basic_level_min(concept, context, upper_neighbors, lower_neighbors,
                    cohesion_function, similarity_function):
    return _bl_helper(
        concept,
        context,
        upper_neighbors,
        lower_neighbors,
        cohesion_function,
        similarity_function,
        variant='min')


@metadata(name='Average Basic Level', short_name='BL_avg', latex='BL_\\mathrm{avg}')
def basic_level_avg(concept, context, upper_neighbors, lower_neighbors,
                    cohesion_function, similarity_function):
    return _bl_helper(
        concept,
        context,
        upper_neighbors,
        lower_neighbors,
        cohesion_function,
        similarity_function,
        variant='avg')
