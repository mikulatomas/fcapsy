from fcapsy import Lattice, Context, Concept
from fcapsy.similarity import jaccard
from fcapsy.algorithms.rice_siff import concept_subset

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


def test_rice_siff_algorithm():
    lattice = Lattice.from_context(context)
    concepts = concept_subset(context, jaccard)

    for concept in concepts:
        assert concept in lattice.concepts
