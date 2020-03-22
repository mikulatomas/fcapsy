import pytest
from fcapy.tools import __load_items_from_file, load_sparse_csv
from bitsets import bitset


def test_load_items_from_file(tmp_path):
    content = "a\nb\nc"

    p = tmp_path / "hello.txt"
    p.write_text(content)

    assert __load_items_from_file(p) == ['a', 'b', 'c']


def test_load_sparse_csv(tmp_path):
    attributes = "a\nb\nc\n"
    dataset = "1,b,c\n2,a,c\n3,a"

    filename_attributes = tmp_path / "attributes"
    filename_dataset = tmp_path / "dataset.csv"

    filename_attributes.write_text(attributes)
    filename_dataset.write_text(dataset)

    Objects_target = bitset('Objects', ('1', '2', '3'))
    Attributes_target = bitset('Attributes', ('a', 'b', 'c'))
    bools_target = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 0],
    ]

    Objects, Attributes, bools = load_sparse_csv(
        filename_dataset,
        filename_attributes
    )

    assert bools == bools_target
    assert Objects.supremum == Objects_target.supremum
    assert Attributes.supremum == Attributes_target.supremum
