import pytest
from bitsets import bitset
from fcapsy import Concept, Context
from fcapsy.psychology.typicality import typicality_avg_without_core
from fcapsy.similarity import jaccard, smc, rosch


@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
def test_objs_typicality_avg_without_core_1(similarity_function):
    context = Context([[1, 1, 0, 0],
                       [0, 1, 0, 0],
                       [0, 1, 1, 0],
                       [0, 1, 0, 1]], range(4), range(4))

    concept = Concept.from_extent(list(range(4)), context)

    objects = tuple(map(lambda x: x.difference(
        concept.intent), context.filter(concept.extent)))

    similarities = (similarity_function(objects[0], objects[0]),
                    similarity_function(objects[0], objects[1]),
                    similarity_function(objects[0], objects[2]),
                    similarity_function(objects[0], objects[3]))

    expected = sum(similarities) / len(objects)

    assert typicality_avg_without_core(
        0, concept, context, similarity_function) == expected
