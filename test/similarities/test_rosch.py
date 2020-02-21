import pytest
from bitsets import bitset
from fcapy.similarity import similarity_rosch


@pytest.fixture
def Attributes():
    universum = range(5)
    Attribtes = bitset('Attributes', universum)

    return Attribtes


def test_normal(Attributes):
    attrs1 = Attributes.frommembers([0, 1, 2])
    attrs2 = Attributes.frommembers([0, 1, 3])

    assert similarity_rosch(attrs1, attrs2) == 2 / 5


def test_disjunct(Attributes):
    attrs1 = Attributes.frommembers([2])
    attrs2 = Attributes.frommembers([0, 1, 3])

    assert similarity_rosch(attrs1, attrs2) == 0 / 5


def test_similarity_jaccard_info():
    assert similarity_rosch.display_name == 'RM'
