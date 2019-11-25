def similarity_smc(attrs1, attrs2, attributes_to_remove=None, cache=None):
    if attributes_to_remove is None:
        attributes_to_remove = attrs1.infimum

    intersection = attrs1.fromint(
        attrs1 & attrs2).difference(attributes_to_remove)

    union = attrs1.fromint(attrs1 | attrs2)

    universum = attrs1.supremum
    complement = universum.difference(attributes_to_remove)
    complement = complement.difference(union)

    try:
        result = (len(intersection) + len(complement)) / \
            len(universum.difference(attributes_to_remove))
    except ZeroDivisionError:
        result = 1

    return result


def similarity_jaccard(attrs1, attrs2, attributes_to_remove=None, cache=None):
    if attributes_to_remove is None:
        attributes_to_remove = attrs1.infimum

    intersection = attrs1.fromint(
        attrs1 & attrs2).difference(attributes_to_remove)

    union = attrs1.fromint(attrs1 | attrs2).difference(attributes_to_remove)

    try:
        result = len(intersection) / len(union)
    except ZeroDivisionError:
        result = 1

    return result
