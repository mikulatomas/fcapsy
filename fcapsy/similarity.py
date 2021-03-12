# Similarities implementation
#
# Belohlavek, Radim, and Martin Trnecka.
# "Basic level in formal concept analysis: Interesting concepts and psychological ramifications."
# Twenty-Third International Joint Conference on Artificial Intelligence. 2013.
#
# Belohlavek, Radim, and Martin Trnecka.
# "Basic level of concepts in formal concept analysis."
# International Conference on Formal Concept Analysis. Springer, Berlin, Heidelberg, 2012.
#
# Rosch, Eleanor, and Carolyn B. Mervis.
# "Family resemblances: Studies in the internal structure of categories."
# Cognitive psychology 7.4 (1975): 573-605.

from fcapsy.decorators import metadata


@metadata(name='Simple Matching Coefficient', short_name='SMC')
def smc(set1, set2):

    intersection = set1.fromint(set1 & set2)

    union = set1.fromint(set1 | set2)

    universum = set1.supremum
    complement = universum.difference(union)

    return (len(intersection) + len(complement)) / len(universum)


@metadata(name='Sørensen–Dice Coefficient', short_name='DSC')
def dsc(set1, set2):

    intersection = set1.fromint(set1 & set2)

    return (2 * len(intersection)) / (len(set1) + len(set2))


@metadata(name='Overlap Coefficient', short_name='Overlap')
def overlap(set1, set2):

    intersection = set1.fromint(set1 & set2)

    return len(intersection) / min(len(set1), len(set2))


@metadata(name='Jaccard', short_name='J')
def jaccard(set1, set2):

    intersection = set1.fromint(set1 & set2)

    union = set1.fromint(set1 | set2)

    return len(intersection) / len(union)


@metadata(name='Rosch', short_name='R')
def rosch(set1, set2):

    intersection = set1.fromint(set1 & set2)

    universum = set1.supremum

    return len(intersection) / len(universum)
