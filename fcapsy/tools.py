import typing


def mean(iterator: typing.Iterator) -> float:
    """Calculate mean value of values from given iterator.

    Example:
        >>> iterator = map(lambda x: x, range(3))
        >>> mean(iterator)
        1.0
    """
    n = 0
    sum_ = 0.0
    for value in iterator:
        sum_ += value
        n += 1

    return sum_ / n
