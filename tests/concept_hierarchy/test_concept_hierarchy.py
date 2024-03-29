import pytest
import pandas as pd

from fcapsy import ConceptHierarchy, Context, Concept
from fcapsy.algorithms.fcbo import fcbo

object_labels = tuple(range(5))
attribute_labels = tuple(range(4))
bools = (
    (1, 0, 0, 0),
    (1, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 1, 0, 0),
    (0, 0, 1, 0),
)
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
        'superordinate': [[1, 3], [0, 1, 2]],
        'subordinate': []
    },
    (0, 1, 2): {
        'superordinate': [[2], [0, 1]],
        'subordinate': [[0, 1, 2, 3]]
    },
    (0, 1): {
        'superordinate': [[1], [0]],
        'subordinate': [[0, 1, 2]]
    },
    (1, 3): {
        'superordinate': [[1]],
        'subordinate': [[0, 1, 2, 3]]
    },
    (1,): {
        'superordinate': [[]],
        'subordinate': [[0, 1], [1, 3]]
    },
    (0,): {
        'superordinate': [[]],
        'subordinate': [[0, 1]]
    },
    (2,): {
        'superordinate': [[]],
        'subordinate': [[0, 1, 2]]
    },
    tuple([]): {
        'superordinate': [],
        'subordinate': [[0], [1], [2]]
    }
}


@pytest.mark.parametrize("alg", ['concept_cover', 'lindig'])
def test_hierarchy_concepts(alg):
    hierarchy = ConceptHierarchy.from_context(context, algorithm=alg)

    expected_concepts = [Concept.from_intent(intent, context)
                         for intent in expected_intents]

    for concept in hierarchy.concepts:
        assert concept in expected_concepts

    assert len(hierarchy.concepts) == 8


@pytest.mark.parametrize("alg, n_of_workers", [('concept_cover', 1), ('concept_cover', 2), ('lindig', 1)])
def test_hierarchy_order_from_context(alg, n_of_workers):
    hierarchy = ConceptHierarchy.from_context(
        context, algorithm=alg, n_of_workers=n_of_workers)

    for intent, neighbors in expected_order.items():
        concept = Concept.from_intent(intent, context)

        for subordinate in neighbors['subordinate']:
            assert concept.from_intent(
                subordinate, context) in hierarchy.subordinate(concept)

        for superordinate in neighbors['superordinate']:
            assert concept.from_intent(
                superordinate, context) in hierarchy.superordinate(concept)


def test_hierarchy_order_from_concepts():
    concepts = fcbo(context)
    hierarchy = ConceptHierarchy.from_concepts(concepts, context)

    for intent, neighbors in expected_order.items():
        concept = Concept.from_intent(intent, context)

        for subordinate in neighbors['subordinate']:
            assert concept.from_intent(
                subordinate, context) in hierarchy.subordinate(concept)

        for superordinate in neighbors['superordinate']:
            assert concept.from_intent(
                superordinate, context) in hierarchy.superordinate(concept)


random_data = [Context.from_random(20, 10) for i in range(10)]


@pytest.mark.parametrize("context", random_data)
def test_random_hierarchies(context):
    hierarchy_lindig = ConceptHierarchy.from_context(
        context, algorithm='lindig')
    hierarchy_concept_cover = ConceptHierarchy.from_context(
        context, algorithm='concept_cover')

    assert hierarchy_lindig == hierarchy_concept_cover


def test_hierarchy_to_json_from_json(tmpdir):
    json_hierarchy = tmpdir.join("test.json")

    hierarchy = ConceptHierarchy.from_context(context)
    hierarchy.to_json(json_hierarchy)

    hierarchy_loaded = ConceptHierarchy.from_json(json_hierarchy, context)

    assert hierarchy == hierarchy_loaded


def test_hierarchy_top():
    hierarchy = ConceptHierarchy.from_context(
        context, algorithm='concept_cover')

    assert hierarchy.top == Concept.from_extent(
        context.Objects.supremum, context)


def test_hierarchy_bottom():
    hierarchy = ConceptHierarchy.from_context(
        context, algorithm='concept_cover')

    assert hierarchy.bottom == Concept.from_extent(
        context.Objects.infimum, context)


def test_hierarchy_from_pandas():
    bools = (
        (1, 0, 0, 0),
        (1, 1, 1, 0),
        (0, 1, 0, 1),
        (1, 1, 0, 0),
        (0, 0, 1, 0),
    )

    df = pd.DataFrame(bools)
    context = Context(bools, df.index, df.columns)

    assert ConceptHierarchy.from_pandas(
        df) == ConceptHierarchy.from_context(context)
