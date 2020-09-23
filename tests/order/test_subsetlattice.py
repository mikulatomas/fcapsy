from fcapy import SubsetLattice, Lattice, Context, Concept
from fcapy.similarity.objects import jaccard

object_labels = tuple(range(5))
attribute_labels = tuple(range(4))
bools = [
    [1, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 0],
    [0, 0, 1, 0],
]
context = Context(bools, object_labels, attribute_labels)


def test_subsetlattice_concepts():
    lattice = Lattice(context)
    subsetlattice = SubsetLattice(context, jaccard)

    for concept in subsetlattice.concepts:
        assert concept in subsetlattice.concepts
