# Similarities implementation
#
# Belohlavek, Radim, and Martin Trnecka. "Basic level in formal concept analysis: Interesting concepts and psychological ramifications."
# Twenty-Third International Joint Conference on Artificial Intelligence. 2013.
#
# Belohlavek, Radim, and Martin Trnecka. "Basic level of concepts in formal concept analysis."
# International Conference on Formal Concept Analysis. Springer, Berlin, Heidelberg, 2012.
#
# Rosch, Eleanor, and Carolyn B. Mervis. "Family resemblances: Studies in the internal structure of categories."
# Cognitive psychology 7.4 (1975): 573-605.

def smc(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    union = attrs1.fromint(attrs1 | attrs2)

    universum = attrs1.supremum
    complement = universum.difference(union)

    return (len(intersection) + len(complement)) / len(universum)


def jaccard(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    union = attrs1.fromint(attrs1 | attrs2)

    return len(intersection) / len(union)


def rosch(attrs1, attrs2):

    intersection = attrs1.fromint(attrs1 & attrs2)

    universum = attrs1.supremum

    return len(intersection) / len(universum)
