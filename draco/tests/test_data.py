import csv
import json

import pandas as pd
import pytest
from draco import data


def test_load_df():
    df = pd.DataFrame({"numbers": [1, 2], "text": ["a", "a"], "bool": [True, False]})
    assert sorted(data.df_to_facts(df)) == sorted(
        [
            ("numberRows", 2),
            ("fieldCardinality", "numbers", 2),
            ("fieldCardinality", "text", 1),
            ("fieldCardinality", "bool", 2),
            ("fieldDataType", "numbers", "number"),
            ("fieldDataType", "text", "string"),
            ("fieldDataType", "bool", "boolean"),
        ]
    )


def test_load_unsupported_data():
    df = pd.DataFrame({"datetime": [pd.Timestamp("20180310")]})
    with pytest.raises(ValueError):
        data.df_to_facts(df)


@pytest.fixture(scope="session")
def csv_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.csv")
    headers = ["numbers", "text"]
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow({"numbers": 1, "text": "a"})
        writer.writerow({"numbers": 2, "text": "a"})
    return str(filename)


def test_csv_to_facts(csv_file):
    assert sorted(data.file_to_facts(csv_file)) == sorted(
        [
            ("numberRows", 2),
            ("fieldCardinality", "numbers", 2),
            ("fieldCardinality", "text", 1),
            ("fieldDataType", "numbers", "number"),
            ("fieldDataType", "text", "string"),
        ]
    )


@pytest.fixture(scope="session")
def json_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.json")
    with open(filename, "w") as f:
        json.dump([{"numbers": 1, "text": "a"}, {"numbers": 2, "text": "a"}], f)
    return str(filename)


def test_json_to_facts(json_file):
    assert sorted(data.file_to_facts(json_file)) == sorted(
        [
            ("numberRows", 2),
            ("fieldCardinality", "numbers", 2),
            ("fieldCardinality", "text", 1),
            ("fieldDataType", "numbers", "number"),
            ("fieldDataType", "text", "string"),
        ]
    )


def test_unknown_file_type():
    with pytest.raises(ValueError):
        data.file_to_facts("foo.bar")
