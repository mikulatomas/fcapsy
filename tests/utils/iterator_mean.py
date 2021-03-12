from fcapsy.utils import iterator_mean


def test_iterator_mean():
    iterator = iter(list(1, 2, 3))
    expected = list(1, 2, 3)

    assert iterator_mean(iterator) == sum(expected) / len(expected)
