import pytest
from bitsets import bitset
from fcapy.psychology.typicality import typicality_rosch, typicality_rosch_ln
from fcapy import Concept, Context
from itertools import compress
import math


def test_typicality_rosch_1():
    context = Context([[1, 1, 1, 1]], range(1), range(4))

    concept = Concept.from_extent(range(0), context)

    weights = [1, 1, 1, 1]

    assert typicality_rosch(0, concept, context) == sum(weights)

    assert typicality_rosch_ln(0, concept, context) == sum(
        [math.log(x) for x in weights])


def test_typicality_rosch_2():
    context = Context([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]], range(4), range(4))

    concept = Concept.from_extent(list(range(4)), context)

    objects = tuple(context.filter(concept.extent))

    weights = [1, 1, 1, 1]

    assert typicality_rosch(0, concept, context) == sum(
        compress(weights, objects[0].bools()))

    assert typicality_rosch_ln(0, concept, context) == sum(
        compress([math.log(x) for x in weights], objects[0].bools()))


def test_typicality_rosch_3():
    context = Context([[1, 1, 1, 1],
                       [1, 0, 1, 0],
                       [0, 0, 0, 1]], range(3), range(4))

    concept = Concept.from_extent(list(range(3)), context)

    objects = tuple(context.filter(concept.extent))

    weights = [2, 1, 2, 2]

    assert typicality_rosch(0, concept, context) == sum(
        compress(weights, objects[0].bools()))
    assert typicality_rosch(1, concept, context) == sum(
        compress(weights, objects[1].bools()))
    assert typicality_rosch(2, concept, context) == sum(
        compress(weights, objects[2].bools()))

    assert typicality_rosch_ln(0, concept, context) == sum(
        compress([math.log(x) for x in weights], objects[0].bools()))
    assert typicality_rosch_ln(1, concept, context) == sum(
        compress([math.log(x) for x in weights], objects[1].bools()))
    assert typicality_rosch_ln(2, concept, context) == sum(
        compress([math.log(x) for x in weights], objects[2].bools()))


def test_typicality_rosch_4():
    context = Context([[0, 0, 0, 0],
                       [1, 1, 1, 1]], range(2), range(4))

    concept = Concept.from_extent(list(range(2)), context)

    objects = tuple(context.filter(concept.extent))

    weights = [1, 1, 1, 1]

    assert typicality_rosch(0, concept, context) == sum(
        compress(weights, objects[0].bools()))

    assert typicality_rosch_ln(0, concept, context) == sum(
        compress([math.log(x) for x in weights], objects[0].bools()))
