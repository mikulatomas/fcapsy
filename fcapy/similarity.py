from .decorators import info


@info('SMC')
def similarity_smc(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    union = attrs1.fromint(attrs1 | attrs2)

    universum = attrs1.supremum
    complement = universum.difference(union)

    return (len(intersection) + len(complement)) / len(universum)


@info('Jaccard')
def similarity_jaccard(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    union = attrs1.fromint(attrs1 | attrs2)

    return len(intersection) / len(union)


@info('RM')
def similarity_rosch(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    universum = attrs1.supremum

    return len(intersection) / len(universum)
