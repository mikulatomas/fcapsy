from fcapy import Context
from bitsets import bitset


def test_context_bools():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.to_bools()) == bools


def test_context_filter_rows():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.filter(context._Objects.frommembers(
        ['a'])))[0] == context._Attributes.frommembers(['2'])


def test_context_filter_columns():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.filter(context._Attributes.frommembers(
        ['1'])))[0] == context._Objects.frommembers(['b'])


def test_context_bools_shape():
    bools = ((0, 1), (1, 1), (0, 1))
    objects = ('a', 'b', 'c')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.shape == (3, 2)


def test_context_to_bools():
    bools = ((0, 1), (1, 1), (0, 1))
    objects = ('a', 'b', 'c')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.to_bools()) == bools


def test_context_up():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.up(context._Objects.frommembers(
        'a')) == context._Attributes.frommembers('2')


def test_context_up_empty():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.up(context._Objects.infimum) == context._Attributes.supremum


def test_context_down():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.down(context._Attributes.frommembers(
        '2')) == context._Objects.frommembers(['a', 'b'])


def test_context_down_empty():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.down(
        context._Attributes.infimum) == context._Objects.supremum
