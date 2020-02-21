import pytest
from bitsets import bitset
from fcapy.typicality import typicality_rosch, typicality_avg, typicality_min
from fcapy import Concept, Context


# def test_find_zero_attributes():
#     universum = range(5)
#     Attributes = bitset('Attributes', universum)

#     objects = [
#         Attributes.frommembers([0, 1, 2, 3]),
#         Attributes.frommembers([0, 2]),
#         Attributes.frommembers([3])
#     ]

#     assert _find_zero_items(objects) == Attributes.frommembers([4])


def test_typicality_rosch():
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
        Attributes.frommembers([0, 2]),
        Attributes.frommembers([3])
    ]

    assert typicality_rosch(objects[0], objects) == 7
    assert typicality_rosch(objects[1], objects) == 4
    assert typicality_rosch(objects[2], objects) == 2


def test_typicality_info():
    assert typicality_rosch.display_name == 'Rosch'
    assert typicality_avg.display_name == 'Typ⌀'
    assert typicality_min.display_name == 'Typ⋀'
