from .decorators import info


@info('SMC')
def similarity_smc(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    union = attrs1.fromint(attrs1 | attrs2)

    universum = attrs1.supremum
    complement = universum.difference(union)

    try:
        result = (len(intersection) + len(complement)) / len(universum)
    except ZeroDivisionError:
        result = 1

    return result


@info('Jaccard')
def similarity_jaccard(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    union = attrs1.fromint(attrs1 | attrs2)

    try:
        result = len(intersection) / len(union)
    except ZeroDivisionError:
        result = 1

    return result


@info('RM')
def similarity_rosch(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    universum = attrs1.supremum

    try:
        result = len(intersection) / len(universum)
    except ZeroDivisionError:
        result = 1

    return result
