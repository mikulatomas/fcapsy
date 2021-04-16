from fcapsy import Context, Concept
from bitsets import bitset
from fcapsy.algorithms.lindig import superordinate_concepts, subordinate_concepts

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


def test_superordinate_concepts():
    concept = Concept(context.Objects.frommembers(
        [1, 3]), context.Attributes.frommembers([0, 1]))

    calculated_superordinate_concepts = tuple(
        superordinate_concepts(context, concept))
    expected_concepts = [
        Concept(
            context.Objects.frommembers([1, 2, 3]),
            context.Attributes.frommembers([1])),
        Concept(
            context.Objects.frommembers([0, 1, 3]),
            context.Attributes.frommembers([0]))
    ]

    assert len(calculated_superordinate_concepts) == 2
    for concept in expected_concepts:
        assert concept in calculated_superordinate_concepts


def test_subordinate_concepts():
    concept = Concept(context.Objects.frommembers(
        [1, 3]), context.Attributes.frommembers([0, 1]))

    calculated_subordinate_concepts = tuple(
        subordinate_concepts(context, concept))
    expected_concepts = [
        Concept(
            context.Objects.frommembers([1]),
            context.Attributes.frommembers([0, 1, 2])),
    ]

    assert len(calculated_subordinate_concepts) == 1
    for concept in expected_concepts:
        assert concept in calculated_subordinate_concepts
