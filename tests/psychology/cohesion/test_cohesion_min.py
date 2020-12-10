import pytest
from fcapy.similarity.objects import jaccard, smc, rosch
from fcapy.psychology.cohesion import cohesion_min
from fcapy import Concept, Context


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_cohesion_singleton_min(similarity_function):
    bools = (
        (1, 0, 1),
        (1, 1, 1),
        (0, 0, 1)
    )

    context = Context(bools, range(3), range(3))

    concept = Concept.from_extent_members([0], context)

    assert cohesion_min(concept, context, similarity_function) == 1


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_cohesion_min(similarity_function):
    bools = (
        (1, 0, 1),
        (1, 1, 1),
        (0, 0, 1)
    )

    context = Context(bools, range(3), range(3))

    concept = Concept.from_extent_members([0, 1], context)

    rows = context.filter_rows_by_extent(concept.extent)

    expected_typ = min(
        similarity_function(rows[0], rows[0]),
        similarity_function(rows[0], rows[1]),
        similarity_function(rows[1], rows[1]))

    assert cohesion_min(
        concept, context, similarity_function) == expected_typ


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_cohesion_min_2(similarity_function):
    bools = (
        (1, 0, 1),
        (1, 1, 1),
        (0, 0, 1)
    )

    context = Context(bools, range(3), range(3))

    concept = Concept.from_extent_members([0, 1, 2], context)

    rows = context.filter_rows_by_extent(concept.extent)

    expected_typ = min(
        similarity_function(rows[0], rows[0]),
        similarity_function(rows[1], rows[1]),
        similarity_function(rows[2], rows[2]),
        similarity_function(rows[0], rows[1]),
        similarity_function(rows[0], rows[2]),
        similarity_function(rows[1], rows[2]),
    )

    assert cohesion_min(
        concept, context, similarity_function) == expected_typ
