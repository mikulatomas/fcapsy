# import pytest
# from fcapy.dataset import generate_random_boolean_dataset
# from fcapy.similarity import similarity_smc
# from fcapy.cohesion import cohesion_min
# from fcapy.basic_level import basic_level_avg
# from fcapy import Context, Lattice


# @pytest.fixture
# def context():
#     Objects, Attributes, bools = generate_random_boolean_dataset(20, 20, 0.20)

#     context = Context(bools, Objects, Attributes)

#     return context


# @pytest.mark.benchmark()
# def test_b_basic_level(benchmark, context):
#     lattice = Lattice(context)

#     def bench():
#         for concept in lattice.get_concepts():
#             upper = lattice.get_upper(concept)
#             lower = lattice.get_lower(concept)

#             basic_level = basic_level_avg(concept, context, upper, lower,
#                                           cohesion_min, similarity_smc)

#     benchmark(bench)


# @pytest.mark.benchmark()
# def test_b_basic_level_cache(benchmark, context):
#     lattice = Lattice(context)

#     cache = {}

#     def bench():
#         for concept in lattice.get_concepts():
#             upper = lattice.get_upper(concept)
#             lower = lattice.get_lower(concept)

#             basic_level = basic_level_avg(concept, context, upper, lower,
#                                           cohesion_min, similarity_smc, cache=cache)

#     benchmark(bench)
