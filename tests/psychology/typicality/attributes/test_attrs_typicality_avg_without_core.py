import pytest
from bitsets import bitset
from fcapsy import Concept, Context
from fcapsy.psychology.typicality import typicality_avg_without_core
from fcapsy.similarity import jaccard, smc, rosch


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_attrs_typicality_avg_without_core_1(similarity_function):
    context = Context([[1, 1, 1, 1],
                       [0, 1, 1, 0],
                       [0, 0, 1, 0],
                       [1, 1, 0, 1]], range(4), range(4))

    concept = Concept.from_intent(list(range(4)), context)

    attributes = tuple(map(lambda x: x.difference(
        concept.extent), context.filter(concept.intent, axis=1)))

    similarities = (similarity_function(attributes[0], attributes[0]),
                    similarity_function(
                        attributes[0], attributes[1]),
                    similarity_function(
                        attributes[0], attributes[2]),
                    similarity_function(attributes[0], attributes[3]))

    expected = sum(similarities) / len(attributes)

    assert typicality_avg_without_core(
        0, concept, context, similarity_function, axis=1) == expected
