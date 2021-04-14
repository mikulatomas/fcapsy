from fcapsy import Concept
from bitsets import bitset


def test_concept_shape():
    Objects = bitset('Objects', range(3))
    Attributes = bitset('Attributes', range(2))

    return Concept(Objects.supremum, Attributes.supremum).shape == (3, 2)


def test_concept_shape2():
    Objects = bitset('Objects', range(2))
    Attributes = bitset('Attributes', range(3))

    return Concept(Objects.supremum, Attributes.supremum).shape == (2, 3)


def test_concept_shape_zero():
    Objects = bitset('Objects', range(3))
    Attributes = bitset('Attributes', range(2))

    return Concept(Objects.supremum, Attributes.infimum).shape == (3, 0)
