import pytest
import pandas as pd

from fcapsy import ConceptHierarchy, Context


def test_concept_hierarchy_eq():
    bools = (
        (1, 0, 0, 0),
        (1, 1, 1, 0),
        (0, 1, 0, 1),
        (1, 1, 0, 0),
        (0, 0, 1, 0),
    )
    context = Context(bools, range(len(bools)), range(len(bools[0])))

    hierarchy1 = ConceptHierarchy.from_context(context)
    hierarchy2 = ConceptHierarchy.from_context(context)

    assert hierarchy1 == hierarchy2


def test_concept_hierarchy_not_eq():
    bools1 = (
        (1, 0, 0, 0),
        (1, 1, 1, 0),
        (0, 1, 0, 1),
        (1, 1, 0, 0),
        (0, 0, 1, 0),
    )

    bools2 = (
        (1, 0, 0, 0),
        (1, 1, 1, 0),
        (0, 1, 0, 1),
        (1, 1, 1, 1),
        (0, 0, 1, 0),
    )

    context1 = Context(bools1, range(len(bools1)), range(len(bools1[0])))
    context2 = Context(bools2, range(len(bools2)), range(len(bools2[0])))

    hierarchy1 = ConceptHierarchy.from_context(context1)
    hierarchy2 = ConceptHierarchy.from_context(context2)

    assert hierarchy1 != hierarchy2
