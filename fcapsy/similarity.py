import typing

import bitsets

__all__ = ["jaccard", "smc", "rosch"]


def jaccard(x: "bitsets.bases.BitSet", y: "bitsets.bases.BitSet") -> float:
    """Jaccard index for two sets.

    Jaccard disregards non-presence.

    Example:
        >>> from bitsets import bitset
        >>> Vector = bitset('Vector', range(10))
        >>> jaccard(Vector([1]), Vector([1]))
        1.0
        >>> jaccard(Vector([1, 2]), Vector([1]))
        0.5
    """
    Vector = type(x)

    intersection = Vector.fromint(x & y)
    union = Vector.fromint(x | y)

    return intersection.count() / union.count()


def smc(x: "bitsets.bases.BitSet", y: "bitsets.bases.BitSet") -> float:
    """Simple matching coefficient (SMC) for two sets.

    SMC treats both presence and non-presence symmetrically.

    Example:
        >>> from bitsets import bitset
        >>> Vector = bitset('Vector', range(10))
        >>> smc(Vector([1]), Vector([1]))
        1.0
        >>> smc(Vector([1, 2]), Vector([1]))
        0.9
    """
    Vector = type(x)

    intersection = Vector.fromint(x & y)
    union = x | y

    universum = Vector.supremum

    complement = Vector.fromint(universum & ~union)

    return (intersection.count() + complement.count()) / universum.count()


def rosch(x: "bitsets.bases.BitSet", y: "bitsets.bases.BitSet") -> float:
    """Warning, this is not a metric. Identity axiom is not satisfied.

    This function is mainly used for calculating typicality. For more details see:

    Belohlavek, Radim, and Mikula, Tomas.
    Typicality in Conceptual Structures Within the Framework of Formal Concept Analysis.
    Proceedings of CLA 2020 (2020): 33-45.

    Example:
        >>> from bitsets import bitset
        >>> Vector = bitset('Vector', range(10))
        >>> rosch(Vector([1]), Vector([1]))
        0.1
        >>> rosch(Vector([1, 2]), Vector([1]))
        0.1
    """
    Vector = type(x)

    intersection = Vector.fromint(x & y)
    universum = Vector.supremum

    return intersection.count() / universum.count()
