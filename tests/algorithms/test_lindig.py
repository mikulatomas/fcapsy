from fcapsy import Context, Concept
from bitsets import bitset
from fcapsy.algorithms.lindig import upper_neighbors, lower_neighbors

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


def test_upper_neighbors():
    concept = Concept(context.Objects.frommembers(
        [1, 3]), context.Attributes.frommembers([0, 1]))

    upper_concepts = tuple(upper_neighbors(context, concept))
    expected_concepts = [
        Concept(
            context.Objects.frommembers([1, 2, 3]),
            context.Attributes.frommembers([1])),
        Concept(
            context.Objects.frommembers([0, 1, 3]),
            context.Attributes.frommembers([0]))
    ]

    assert len(upper_concepts) == 2
    for concept in expected_concepts:
        assert concept in upper_concepts


def test_lower_neighbors():
    concept = Concept(context.Objects.frommembers(
        [1, 3]), context.Attributes.frommembers([0, 1]))

    lower_concepts = tuple(lower_neighbors(context, concept))
    expected_concepts = [
        Concept(
            context.Objects.frommembers([1]),
            context.Attributes.frommembers([0, 1, 2])),
    ]

    assert len(lower_concepts) == 1
    for concept in expected_concepts:
        assert concept in lower_concepts
