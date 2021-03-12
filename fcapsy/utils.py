def iterator_mean(iterator):
    n = 0
    sum_value = 0.0
    for value in iterator:
        sum_value += value
        n += 1

    return sum_value / n
