from fcapy import Context
from bitsets import bitset


def test_context_bools():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    assert context.get_bools() == bools


def test_context_up():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    assert context.up(Objects.frommembers('a')) == Attributes.frommembers('2')


def test_context_down():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    assert context.down(Attributes.frommembers(
        '2')) == Objects.frommembers(['a', 'b'])
