from fcapsy import Concept, Context
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


def test_concept_ratio():
    Objects = bitset('Objects', range(3))
    Attributes = bitset('Attributes', range(2))

    return Concept(Objects.supremum, Attributes.supremum).ratio == 3 / 2


def test_concept_ratio2():
    Objects = bitset('Objects', range(2))
    Attributes = bitset('Attributes', range(3))

    return Concept(Objects.supremum, Attributes.supremum).ratio == 2 / 3


def test_concept_ratio_zero():
    Objects = bitset('Objects', range(3))
    Attributes = bitset('Attributes', range(2))

    return Concept(Objects.supremum, Attributes.infimum).ratio == 0
