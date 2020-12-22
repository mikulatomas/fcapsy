from fcapy import Concept, Context
from bitsets import bitset


def test_concept_repr():
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2', '3'))

    concept = Concept(Objects(['a', 'b']), Attributes(['3']))

    assert repr(concept) == "Concept(2x1)"


def test_concept_str():
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2', '3'))

    concept = Concept(Objects(['a', 'b']), Attributes(['3']))

    assert str(concept) == "Concept(('a', 'b'), ('3',))"


def test_concept_from_intent():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    expected_concept = Concept(
        context.Objects.frommembers(['b']),
        context.Attributes.frommembers(['1', '2']))

    concept = Concept.from_intent(
        context.Attributes.frommembers(['1']), context)

    assert concept == expected_concept


def test_concept_from_intent2():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    expected_concept = Concept(
        context.Objects.frommembers(['b']),
        context.Attributes.frommembers(['1', '2']))

    concept = Concept.from_intent(['1'], context)

    assert concept == expected_concept


def test_concept_from_extent():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    expected_concept = Concept(
        context.Objects.frommembers(['b']),
        context.Attributes.frommembers(['1', '2']))

    concept = Concept.from_extent(
        context.Objects.frommembers(['b']), context)

    assert concept == expected_concept


def test_concept_from_extent2():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    expected_concept = Concept(
        context.Objects.frommembers(['b']),
        context.Attributes.frommembers(['1', '2']))

    concept = Concept.from_extent(['b'], context)

    assert concept == expected_concept
