import pytest
from bitsets import bitset
from fcapsy import Concept, Context
from fcapsy.psychology.typicality import typicality_min
from fcapsy.similarity import jaccard, smc, rosch


@pytest.mark.parametrize("similarity_function", [jaccard, smc])
def test_attrs_typicality_min_1(similarity_function):
    context = Context([[1, 0, 0, 0]], range(1), range(4))
    concept = Concept.from_intent([0], context)

    assert typicality_min(0, concept, context, similarity_function) == 1


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_attrs_typicality_min_2(similarity_function):

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

    expected = min(similarities)

    assert typicality_min(0, concept, context,
                          similarity_function, axis=1) == expected


@ pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_attrs_typicality_min_3(similarity_function):
    context = Context([[1, 1, 1],
                       [1, 0, 1],
                       [0, 0, 0],
                       [1, 1, 0]], range(4), range(3))

    concept = Concept.from_intent(list(range(3)), context)

    attributes = tuple(context.filter(concept.intent, axis=1))

    similarities = (similarity_function(attributes[0], attributes[0]),
                    similarity_function(attributes[0], attributes[1]),
                    similarity_function(attributes[0], attributes[2]))

    expected = min(similarities)

    assert typicality_min(0, concept, context,
                          similarity_function, axis=1) == expected


@ pytest.mark.parametrize("similarity_function", [smc, rosch])
def test_attrs_typicality_min_4(similarity_function):
    context = Context([[0, 1],
                       [0, 1],
                       [0, 1],
                       [0, 1]], range(4), range(2))

    concept = Concept.from_intent(list(range(2)), context)

    attributes = tuple(context.filter(concept.intent, axis=1))

    similarities = (similarity_function(attributes[0], attributes[0]),
                    similarity_function(attributes[0], attributes[1]))

    expected = min(similarities)

    assert typicality_min(0, concept, context,
                          similarity_function, axis=1) == expected
