from fcapsy import Context
from bitsets import bitset
from tests import load_all_test_files
import os
import pytest
import json
import pandas as pd

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
    assert list(context.Attributes.supremum.members(
    )) == expected_json['attributes']
    assert list(context.Objects.supremum.members(
    )) == expected_json['objects']
    assert tuple(context.to_bools()) == tuple(
        map(tuple, expected_json['bools']))


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
    assert list(context.Attributes.supremum.members(
    )) == expected_json['attributes']
    assert list(context.Objects.supremum.members(
    )) == expected_json['objects']
    assert tuple(context.to_bools()) == tuple(
        map(tuple, expected_json['bools']))


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
    assert list(context.Attributes.supremum.members(
    )) == expected_json['attributes']
    assert list(context.Objects.supremum.members(
    )) == expected_json['objects']
    assert tuple(context.to_bools()) == tuple(
        map(tuple, expected_json['bools']))


def test_context_from_pandas():
    bools = (
        (2, 0, 6),
        (132, 1, 0)
    )

    expected_bools = (
        (1, 0, 1),
        (1, 1, 0)
    )

    context = Context.from_pandas(pd.DataFrame(bools))

    assert tuple(context.to_bools()) == expected_bools


def test_context_from_pandas_truth_values():
    bools = (
        (2, 0, 6),
        (132, 1, 0)
    )

    expected_bools = (
        (0, 0, 1),
        (1, 0, 0)
    )

    df = pd.DataFrame(bools)

    context = Context.from_pandas(df > 2)

    assert tuple(context.to_bools()) == expected_bools
