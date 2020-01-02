from fcapy import Lattice, Context
from bitsets import bitset


def test_lattice_creation():
    bools = ((0, 1), (1, 1))
    Objects = bitset('Objects', ('a', 'b'))
    Attributes = bitset('Attributes', ('1', '2'))

    context = Context(bools, Objects, Attributes)

    lattice = Lattice(context)

    assert len(lattice.get_concepts()) == 2
