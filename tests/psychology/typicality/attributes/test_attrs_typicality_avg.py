import pytest
from bitsets import bitset
from fcapy import Concept, Context
from fcapy.psychology.typicality import typicality_avg
from fcapy.similarity import jaccard, smc, rosch


@pytest.mark.parametrize("similarity_function", [jaccard, smc])
def test_attrs_typicality_avg_1(similarity_function):
    context = Context([[[1],
                        [0],
                        [0],
                        [0]]], range(4), range(1))
    concept = Concept.from_intent([0], context)

    assert typicality_avg(0, concept, context,
                          similarity_function, axis=1) == 1


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_attrs_typicality_avg_2(similarity_function):

    context = Context([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]], range(4), range(4))

    concept = Concept.from_intent(list(range(4)), context)

    attributes = tuple(context.filter(concept.intent, axis=1))

    similarities = (similarity_function(attributes[0], attributes[0]),
                    similarity_function(attributes[0], attributes[1]),
                    similarity_function(attributes[0], attributes[2]),
                    similarity_function(attributes[0], attributes[3]))

    expected = sum(similarities) / len(attributes)

    assert typicality_avg(0, concept, context,
                          similarity_function, axis=1) == expected


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_attrs_typicality_avg_3(similarity_function):
    context = Context([[1, 1, 1],
                       [1, 0, 1],
                       [0, 0, 0],
                       [1, 1, 0], ], range(4), range(3))

    concept = Concept.from_intent(list(range(3)), context)

    attributes = tuple(context.filter(concept.intent, axis=1))

    similarities = (similarity_function(attributes[0], attributes[0]),
                    similarity_function(attributes[0], attributes[1]),
                    similarity_function(attributes[0], attributes[2]))

    expected = sum(similarities) / len(attributes)

    assert typicality_avg(0, concept, context,
                          similarity_function, axis=1) == expected


@ pytest.mark.parametrize("similarity_function", [smc, rosch])
def test_attrs_typicality_avg_4(similarity_function):
    context = Context([[0, 1],
                       [0, 1],
                       [0, 1],
                       [0, 1]], range(4), range(2))

    concept = Concept.from_intent(list(range(2)), context)

    attributes = tuple(context.filter(concept.intent, axis=1))

    similarities = (similarity_function(attributes[0], attributes[0]),
                    similarity_function(attributes[0], attributes[1]))

    expected = sum(similarities) / len(attributes)

    assert typicality_avg(0, concept, context,
                          similarity_function, axis=1) == expected
