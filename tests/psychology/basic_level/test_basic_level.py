import pytest

from fcapy import Context, Lattice
from fcapy.similarity.objects import jaccard, smc, rosch
from fcapy.psychology.cohesion import cohesion_avg, cohesion_min
from fcapy.psychology.basic_level import basic_level_avg, basic_level_min
from itertools import combinations


@pytest.mark.parametrize("basic_level", [basic_level_min])
@pytest.mark.parametrize("similarity_function", [jaccard, smc, rosch])
@pytest.mark.parametrize("cohesion_function", [cohesion_avg, cohesion_min])
def test_basic_level_random_context(basic_level, similarity_function, cohesion_function):
    context = Context.from_random(20, 10)

    lattice = Lattice(context)

    for concept in lattice.concepts:
        basic_level(
            concept, context, lattice[concept].upper, lattice[concept].lower, cohesion_function, similarity_function)
