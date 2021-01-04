import pandas as pd
from draco import Fact, utils
import pytest
import csv
import json


def test_load_df():
    df = pd.DataFrame(
        [[1, "a", True], [2, "a", False]], columns=["numbers", "text", "bool"]
    )
    assert sorted(utils.df_to_facts(df)) == sorted(
        [
            Fact("numberRows", 2),
            Fact("fieldCardinality", ("numbers", 2)),
            Fact("fieldCardinality", ("text", 1)),
            Fact("fieldCardinality", ("bool", 2)),
            Fact("fieldDataType", ("numbers", "number")),
            Fact("fieldDataType", ("text", "string")),
            Fact("fieldDataType", ("bool", "boolean")),
        ]
    )


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
    assert sorted(utils.file_to_facts(csv_file)) == sorted(
        [
            Fact("numberRows", 2),
            Fact("fieldCardinality", ("numbers", 2)),
            Fact("fieldCardinality", ("text", 1)),
            Fact("fieldDataType", ("numbers", "number")),
            Fact("fieldDataType", ("text", "string")),
        ]
    )


@pytest.fixture(scope="session")
def json_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.json")
    with open(filename, "w") as f:
        json.dump([{"numbers": 1, "text": "a"}, {"numbers": 2, "text": "a"}], f)
    return str(filename)


def test_json_to_facts(json_file):
    assert sorted(utils.file_to_facts(json_file)) == sorted(
        [
            Fact("numberRows", 2),
            Fact("fieldCardinality", ("numbers", 2)),
            Fact("fieldCardinality", ("text", 1)),
            Fact("fieldDataType", ("numbers", "number")),
            Fact("fieldDataType", ("text", "string")),
        ]
    )


def test_unknown_file_type():
    with pytest.raises(ValueError):
        utils.file_to_facts("foo.bar")
