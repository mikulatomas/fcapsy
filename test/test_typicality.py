import pytest
from bitsets import bitset
from fcapy.typicality import _find_zero_items, typicality_rosch, typicality_avg, typicality_min
from fcapy import Concept, Context


def test_find_zero_attributes():
    universum = range(5)
    Attributes = bitset('Attributes', universum)

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
        Attributes.frommembers([0, 2]),
        Attributes.frommembers([3])
    ]

    assert _find_zero_items(objects) == Attributes.frommembers([4])


def test_typicality_rosch():
    Attributes = bitset('Attributes', range(4))
    Objects = bitset('Objects', range(3))

    bools = [
        [1, 1, 1, 1],
        [1, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    context = Context(bools, Objects, Attributes)

    concept = Concept(Objects.supremum, Attributes.supremum)

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
        Attributes.frommembers([0, 2]),
        Attributes.frommembers([3])
    ]

    assert typicality_rosch(objects[0], concept, context) == 7
    assert typicality_rosch(objects[1], concept, context) == 4
    assert typicality_rosch(objects[2], concept, context) == 2


def test_typicality_info():
    assert typicality_rosch.display_name == 'Rosch'
    assert typicality_avg.display_name == 'Typ⌀'
    assert typicality_min.display_name == 'Typ⋀'
