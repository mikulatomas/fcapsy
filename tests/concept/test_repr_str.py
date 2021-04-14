from fcapsy import Concept
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
