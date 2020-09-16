from fcapy import Context
from bitsets import bitset


def test_context_bools():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.get_bools() == bools


def test_context_up():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.up(context._Objects.frommembers(
        'a')) == context._Attributes.frommembers('2')


def test_context_down():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.down(context._Attributes.frommembers(
        '2')) == context._Objects.frommembers(['a', 'b'])
