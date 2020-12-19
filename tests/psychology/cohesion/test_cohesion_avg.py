import pytest
from fcapy.similarity.objects import jaccard, smc, rosch
from fcapy.psychology.cohesion import cohesion_avg
from fcapy import Concept, Context


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_cohesion_singleton_avg(similarity_function):
    bools = (
        (1, 0, 0),
        (1, 1, 0),
        (0, 0, 1)
    )

    context = Context(bools, range(3), range(3))

    concept = Concept.from_extent([2], context)

    assert cohesion_avg(concept, context, similarity_function) == 1


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_cohesion_avg(similarity_function):
    bools = (
        (1, 0, 1),
        (1, 1, 1),
        (0, 0, 1)
    )

    context = Context(bools, range(3), range(3))

    concept = Concept.from_extent([0, 1], context)
    print(concept.extent)
    print(concept.intent)
    rows = tuple(context.filter(concept.extent))

    expected_typ = (similarity_function(rows[0], rows[1]) + 2) / (2 * 3 / 2)

    assert cohesion_avg(
        concept, context, similarity_function) == expected_typ


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_cohesion_avg_2(similarity_function):
    bools = (
        (1, 0, 1),
        (1, 1, 1),
        (0, 0, 1)
    )

    context = Context(bools, range(3), range(3))

    concept = Concept.from_extent([0, 1, 2], context)

    rows = tuple(context.filter(concept.extent))

    suma = similarity_function(rows[0], rows[1]) + \
        similarity_function(rows[1], rows[2]) + \
        similarity_function(rows[2], rows[0]) + 3

    expected_typ = suma / (3 * 4 / 2)

    assert cohesion_avg(
        concept, context, similarity_function) == expected_typ
