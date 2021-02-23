import pytest
from fcapy import Context, Lattice
from fcapy.algorithms.fcbo import fcbo
from fcapy.algorithms.rice_siff import concept_subset
from fcapy.similarity import jaccard


random_data = [Context.from_random(20, 10) for i in range(10)]


@pytest.mark.parametrize("context", random_data)
def test_random_alg_test(context):
    fcbo_result = set(fcbo(context))
    lattice_result = set(Lattice(context).concepts)
    subset_result = set(concept_subset(context, jaccard))

    assert fcbo_result == lattice_result
    assert subset_result.issubset(fcbo_result)
