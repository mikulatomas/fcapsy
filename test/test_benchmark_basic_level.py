import pytest
from fcapy.dataset import generate_random_boolean_dataset
from fcapy.order import calculate_lattice, UPPER, LOWER
from fcapy.similarity import similarity_smc
from fcapy.cohesion import cohesion_min
from fcapy.basic_level import basic_level_avg
from fcapy import Context


@pytest.mark.benchmark()
def test_b_basic_level(benchmark):
    Objects, Attributes, bools = generate_random_boolean_dataset(5, 5, 0.20)

    context = Context(bools, Objects, Attributes)
    order = calculate_lattice(context)

    concepts = list(order.keys())

    def bench():
        for concept in concepts:
            upper = order[concept][UPPER]
            lower = order[concept][LOWER]

            basic_level = basic_level_avg(concept, context, upper, lower,
                                          cohesion_min, similarity_smc)

    benchmark(bench)
