from fcapsy import Concept
from bitsets import bitset


def test_concept_size():
    Objects = bitset('Objects', range(3))
    Attributes = bitset('Attributes', range(2))

    return Concept(Objects.supremum, Attributes.supremum).size == 3 * 2


def test_concept_size2():
    Objects = bitset('Objects', range(2))
    Attributes = bitset('Attributes', range(3))

    return Concept(Objects.supremum, Attributes.supremum).size == 3 * 2


def test_concept_size_zero():
    Objects = bitset('Objects', range(3))
    Attributes = bitset('Attributes', range(2))

    return Concept(Objects.supremum, Attributes.infimum).size == 0
