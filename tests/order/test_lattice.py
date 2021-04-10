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
    lattice = Lattice.from_context(context, algorithm=alg)

    expected_concepts = [Concept.from_intent(intent, context)
                         for intent in expected_intents]

    for concept in lattice.concepts:
        assert concept in expected_concepts

    assert len(lattice.concepts) == 8


@pytest.mark.parametrize("alg", ['fcbo', 'lindig'])
def test_lattice_order(alg):
    lattice = Lattice.from_context(context, algorithm=alg)

    for intent, neighbors in expected_order.items():
        concept = Concept.from_intent(intent, context)

        for lower in neighbors['lower']:
            assert concept.from_intent(
                lower, context) in lattice[concept].lower

        for upper in neighbors['upper']:
            assert concept.from_intent(
                upper, context) in lattice[concept].upper


random_data = [Context.from_random(20, 10) for i in range(10)]


@pytest.mark.parametrize("context", random_data)
def test_random_lattices(context):
    lattice_lindig = Lattice.from_context(context, algorithm='lindig')
    lattice_fcbo = Lattice.from_context(context, algorithm='fcbo')

    assert set(lattice_lindig.concepts) == set(lattice_fcbo.concepts)

    for concept in lattice_lindig.concepts:
        assert lattice_fcbo.get(
            concept).upper == lattice_lindig.get(concept).upper
        assert lattice_fcbo.get(
            concept).lower == lattice_lindig.get(concept).lower


def test_lattice_to_json_from_json(tmpdir):
    json_lattice = tmpdir.join("test.json")

    lattice = Lattice.from_context(context)
    lattice.to_json(json_lattice)

    lattice_loaded = Lattice.from_json(json_lattice, context)

    assert set(lattice.concepts) == set(lattice_loaded.concepts)

    for concept in lattice.concepts:
        assert lattice_loaded.get(
            concept).upper == lattice.get(concept).upper
        assert lattice_loaded.get(
            concept).lower == lattice.get(concept).lower
