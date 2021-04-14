from fcapsy import Concept
from bitsets import bitset


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
