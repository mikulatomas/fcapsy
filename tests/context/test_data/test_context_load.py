from fcapy import Context
from bitsets import bitset
from tests import load_all_test_files
import os
import pytest
import json

TEST_DATA_DIR_FIMI = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fimi',
)


@pytest.mark.parametrize("data_file, json_file",
                         load_all_test_files(TEST_DATA_DIR_FIMI))
def test_context_from_fimi(data_file, json_file):

    # Load dataset file
    with open(data_file) as f:
        context = Context.from_fimi(data_file)

    # Load expected output
    with open(json_file) as f:
        expected_json = json.load(f)

    # Compare
    assert list(context._Attributes.supremum.members(
    )) == expected_json['attributes']
    assert list(context._Objects.supremum.members(
    )) == expected_json['objects']
    assert context.get_bools() == tuple(map(tuple, expected_json['bools']))


TEST_DATA_DIR_CSV = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'csv', 'no_parameter'
)


@pytest.mark.parametrize("data_file, json_file",
                         load_all_test_files(TEST_DATA_DIR_CSV))
def test_context_from_csv(data_file, json_file):

    # Load dataset file
    with open(data_file) as f:
        context = Context.from_csv(data_file)

    # Load expected output
    with open(json_file) as f:
        expected_json = json.load(f)

    # Compare
    assert list(context._Attributes.supremum.members(
    )) == expected_json['attributes']
    assert list(context._Objects.supremum.members(
    )) == expected_json['objects']
    assert context.get_bools() == tuple(map(tuple, expected_json['bools']))


TEST_DATA_DIR_CSV_DELIMITER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'csv', 'delimiter'
)


@pytest.mark.parametrize("data_file, json_file",
                         load_all_test_files(TEST_DATA_DIR_CSV_DELIMITER))
def test_context_from_csv_delimiter(data_file, json_file):

    # Load dataset file
    with open(data_file) as f:
        context = Context.from_csv(data_file, delimiter=';')

    # Load expected output
    with open(json_file) as f:
        expected_json = json.load(f)

    # Compare
    assert list(context._Attributes.supremum.members(
    )) == expected_json['attributes']
    assert list(context._Objects.supremum.members(
    )) == expected_json['objects']
    assert context.get_bools() == tuple(map(tuple, expected_json['bools']))
