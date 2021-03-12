from fcapsy import Context
from bitsets import bitset


def test_context_bools():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.to_bools()) == bools


def test_context_repr():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert repr(context) == "Context(2x2)"


def test_context_filter_rows():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.filter(['a']))[
        0] == context.Attributes.frommembers(['2'])


def test_context_filter_columns():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert tuple(context.filter(['1'], axis=1))[
        0] == context.Objects.frommembers(['b'])


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

    assert context.up(context.Objects.frommembers(
        'a')) == context.Attributes.frommembers('2')


def test_context_up_empty():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.up(context.Objects.infimum) == context.Attributes.supremum


def test_context_down():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.down(context.Attributes.frommembers(
        '2')) == context.Objects.frommembers(['a', 'b'])


def test_context_down_empty():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.down(
        context.Attributes.infimum) == context.Objects.supremum


def test_context_density():
    bools = ((0, 1), (1, 0))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.density == 0.5


def test_context_density2():
    bools = ((0, 1), (1, 1))
    objects = ('a', 'b')
    attributes = ('1', '2')

    context = Context(bools, objects, attributes)

    assert context.density == 3 / 4
