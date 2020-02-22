import pytest
from bitsets import bitset
from fcapy.typicality import typicality_rosch, typicality_rosch_ln
from fcapy import Concept, Context
from itertools import compress
import math


def test_typicality_rosch_1():
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
    ]

    weights = [1, 1, 1, 1]

    assert typicality_rosch(objects[0], objects) == sum(weights)

    assert typicality_rosch_ln(objects[0], objects) == sum(
        [math.log(x) for x in weights])


def test_typicality_rosch_2():
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0]),
        Attributes.frommembers([1]),
        Attributes.frommembers([2]),
        Attributes.frommembers([3]),
    ]

    weights = [1, 1, 1, 1]

    assert typicality_rosch(objects[0], objects) == sum(
        compress(weights, objects[0].bools()))

    assert typicality_rosch_ln(objects[0], objects) == sum(
        compress([math.log(x) for x in weights], objects[0].bools()))


def test_typicality_rosch_3():
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([0, 1, 2, 3]),
        Attributes.frommembers([0, 2]),
        Attributes.frommembers([3])
    ]

    weights = [2, 1, 2, 2]

    assert typicality_rosch(objects[0], objects) == sum(
        compress(weights, objects[0].bools()))
    assert typicality_rosch(objects[1], objects) == sum(
        compress(weights, objects[1].bools()))
    assert typicality_rosch(objects[2], objects) == sum(
        compress(weights, objects[2].bools()))

    assert typicality_rosch_ln(objects[0], objects) == sum(
        compress([math.log(x) for x in weights], objects[0].bools()))
    assert typicality_rosch_ln(objects[1], objects) == sum(
        compress([math.log(x) for x in weights], objects[1].bools()))
    assert typicality_rosch_ln(objects[2], objects) == sum(
        compress([math.log(x) for x in weights], objects[2].bools()))


def test_typicality_rosch_4():
    Attributes = bitset('Attributes', range(4))

    objects = [
        Attributes.frommembers([]),
        Attributes.frommembers([0, 1, 2, 3]),
    ]

    weights = [1, 1, 1, 1]

    assert typicality_rosch(objects[0], objects) == sum(
        compress(weights, objects[0].bools()))

    assert typicality_rosch_ln(objects[0], objects) == sum(
        compress([math.log(x) for x in weights], objects[0].bools()))


def test_typicality_info():
    assert typicality_rosch.display_name == 'Rosch'
    assert typicality_rosch_ln.display_name == 'Rosch ln'
