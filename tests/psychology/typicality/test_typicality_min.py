import pytest
from bitsets import bitset
from fcapy import Concept, Context
from fcapy.psychology.typicality import typicality_min
from fcapy.similarity import jaccard, smc, rosch


@pytest.mark.parametrize("similarity_function", [jaccard, smc])
def test_typicality_min_1(similarity_function):
    context = Context([[1, 0, 0, 0]], range(1), range(4))
    concept = Concept.from_extent([0], context)

    assert typicality_min(0, concept, context, similarity_function) == 1


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_typicality_min_2(similarity_function):

    context = Context([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]], range(4), range(4))

    concept = Concept.from_extent(list(range(4)), context)

    objects = tuple(context.filter(concept.extent))

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]),
                    similarity_function(objects[0], objects[2]),
                    similarity_function(objects[0], objects[3]))

    expected = min(similarities)

    assert typicality_min(0, concept, context, similarity_function) == expected


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_typicality_min_3(similarity_function):
    context = Context([[1, 1, 1, 1],
                       [1, 0, 1, 0],
                       [0, 0, 0, 1]], range(3), range(4))

    concept = Concept.from_extent(list(range(3)), context)

    objects = tuple(context.filter(concept.extent))

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]),
                    similarity_function(objects[0], objects[2]))

    expected = min(similarities)

    assert typicality_min(0, concept, context, similarity_function) == expected


@ pytest.mark.parametrize("similarity_function", [smc, rosch])
def test_typicality_min_4(similarity_function):
    context = Context([[0, 0, 0, 0],
                       [1, 1, 1, 1]], range(2), range(4))

    concept = Concept.from_extent(list(range(2)), context)

    objects = tuple(context.filter(concept.extent))

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]))

    expected = min(similarities)

    assert typicality_min(0, concept, context, similarity_function) == expected
