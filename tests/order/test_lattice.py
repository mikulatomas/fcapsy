import pytest

from fcapsy import Lattice, Context, Concept

object_labels = tuple(range(5))
attribute_labels = tuple(range(4))
bools = [
    [1, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 0],
    [0, 0, 1, 0],
]
context = Context(bools, object_labels, attribute_labels)

expected_intents = [
    [0, 1, 2, 3],
    [0, 1, 2],
    [0, 1],
    [1, 3],
    [2],
    [0],
    [1],
    [],
]

expected_order = {
    (0, 1, 2, 3): {
        'upper': [[1, 3], [0, 1, 2]],
        'lower': []
    },
    (0, 1, 2): {
        'upper': [[2], [0, 1]],
        'lower': [[0, 1, 2, 3]]
    },
    (0, 1): {
        'upper': [[1], [0]],
        'lower': [[0, 1, 2]]
    },
    (1, 3): {
        'upper': [[1]],
        'lower': [[0, 1, 2, 3]]
    },
    (1,): {
        'upper': [[]],
        'lower': [[0, 1], [1, 3]]
    },
    (0,): {
        'upper': [[]],
        'lower': [[0, 1]]
    },
    (2,): {
        'upper': [[]],
        'lower': [[0, 1, 2]]
    },
    tuple([]): {
        'upper': [],
        'lower': [[0], [1], [2]]
    }
}


@pytest.mark.parametrize("alg", ['fcbo', 'lindig'])
def test_lattice_concepts(alg):
    lattice = Lattice(context, algorithm=alg)

    expected_concepts = [Concept.from_intent(intent, context)
                         for intent in expected_intents]

    for concept in lattice.concepts:
        assert concept in expected_concepts

    assert len(lattice.concepts) == 8


@pytest.mark.parametrize("alg", ['fcbo', 'lindig'])
def test_lattice_order(alg):
    lattice = Lattice(context, algorithm=alg)

    for intent, neighbors in expected_order.items():
        concept = Concept.from_intent(intent, context)

        for lower in neighbors['lower']:
            assert concept.from_intent(
                lower, context) in lattice[concept].lower

        for upper in neighbors['upper']:
            assert concept.from_intent(
                upper, context) in lattice[concept].upper
