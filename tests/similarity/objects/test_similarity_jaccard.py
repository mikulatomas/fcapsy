import pytest
from bitsets import bitset
from fcapy.similarity import jaccard


@pytest.fixture
def Attributes():
    universum = range(5)
    Attribtes = bitset('Attributes', universum)

    return Attribtes


def test_normal(Attributes):
    attrs1 = Attributes.frommembers([0, 1, 2])
    attrs2 = Attributes.frommembers([0, 1, 3])

    assert jaccard(attrs1, attrs2) == 2 / 4


def test_disjunct(Attributes):
    attrs1 = Attributes.frommembers([2])
    attrs2 = Attributes.frommembers([0, 1, 3])

    assert jaccard(attrs1, attrs2) == 0 / 4
