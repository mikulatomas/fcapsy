import pytest
from bitsets import bitset
from fcapy.cohesion import cohesion_avg, cohesion_min
from fcapy.similarity import similarity_jaccard
from fcapy import Concept, Context


def test_cohesion_avg():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    concept = Concept(Objects(['a', 'b']), Attributes(['2']))

    rows = context.filter_rows_by_extent(concept.extent)

    expected_coh = similarity_jaccard(
        rows[0], rows[1]) / (len(concept.extent) * (len(concept.extent) - 1) / 2)

    assert cohesion_avg(concept, context, similarity_jaccard) == expected_coh


def test_cohesion_avg_2():
    bools = ((0, 1), (1, 1), (0, 1))
    Objects = bitset('Objects', ('a', 'b', 'c'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    concept = Concept(Objects(['a', 'b', 'c']), Attributes(['2']))

    rows = context.filter_rows_by_extent(concept.extent)

    suma = similarity_jaccard(rows[0], rows[1]) + \
        similarity_jaccard(rows[1], rows[2]) + \
        similarity_jaccard(rows[0], rows[2])

    expected_coh = suma / (len(concept.extent) * (len(concept.extent) - 1) / 2)

    assert cohesion_avg(concept, context, similarity_jaccard) == expected_coh


def test_cohesion_min():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    concept = Concept(Objects(['a', 'b']), Attributes(['2']))

    rows = context.filter_rows_by_extent(concept.extent)

    expected_coh = similarity_jaccard(
        rows[0], rows[1])

    assert cohesion_min(concept, context, similarity_jaccard) == expected_coh


def test_cohesion_min_2():
    bools = ((0, 1), (1, 1), (0, 1))
    Objects = bitset('Objects', ('a', 'b', 'c'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    concept = Concept(Objects(['a', 'b', 'c']), Attributes(['2']))

    rows = context.filter_rows_by_extent(concept.extent)

    suma = (similarity_jaccard(rows[0], rows[1]),
            similarity_jaccard(rows[1], rows[2]),
            similarity_jaccard(rows[0], rows[2]))

    expected_coh = min(suma)

    assert cohesion_min(concept, context, similarity_jaccard) == expected_coh
