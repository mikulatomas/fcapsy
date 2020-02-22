import pytest
from bitsets import bitset
from fcapy.similarity import similarity_smc


@pytest.fixture
def Attributes():
    universum = range(5)
    Attribtes = bitset('Attributes', universum)

    return Attribtes


def test_normal(Attributes):
    attrs1 = Attributes.frommembers([0, 1, 2])
    attrs2 = Attributes.frommembers([0, 1, 3])

    assert similarity_smc(attrs1, attrs2) == 3 / 5


def test_disjunct(Attributes):
    attrs1 = Attributes.frommembers([2])
    attrs2 = Attributes.frommembers([0, 1, 3])

    assert similarity_smc(attrs1, attrs2) == (0 + 5 - 4) / 5

# def test_remove_intent(Attributes):
#     attrs1 = Attributes.frommembers([0, 1, 2])
#     attrs2 = Attributes.frommembers([0, 1, 3])
#     intent = Attributes.frommembers([0, 1])

#     assert similarity_smc(attrs1, attrs2, attributes_to_remove=intent) == 1 / 3


# def test_remove_zeros(Attributes):
#     attrs1 = Attributes.frommembers([0, 1, 2])
#     attrs2 = Attributes.frommembers([0, 1, 3])
#     intent = Attributes.frommembers([4])

#     assert similarity_smc(attrs1, attrs2, attributes_to_remove=intent) == 2 / 4


# def test_remove_both(Attributes):
#     attrs1 = Attributes.frommembers([0, 1, 2])
#     attrs2 = Attributes.frommembers([0, 1, 3])
#     intent = Attributes.frommembers([0, 1, 4])

#     assert similarity_smc(attrs1, attrs2, attributes_to_remove=intent) == 0


def test_similarity_smc_info():
    assert similarity_smc.display_name == 'SMC'
