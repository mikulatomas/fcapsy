from fcapy import Context
from bitsets import bitset


def test_context_bools():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    assert context.get_bools() == bools


def test_context_objects_attributes():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    assert context.get_objects() == ('a', 'b')
    assert context.get_attributes() == ('1', '2')
