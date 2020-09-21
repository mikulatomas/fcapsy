from fcapy import Concept
from bitsets import bitset


def test_concept_id():
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2', '3'))

    concept = Concept(Objects(['a']), Attributes(['3']))

    assert concept.get_id() == 4
