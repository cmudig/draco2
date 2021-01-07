import csv
import datetime
import json

import pandas as pd
import pytest
from draco import schema


def test_load_df():
    df = pd.DataFrame(
        {
            "numbers": [1, 2],
            "text": ["a", "a"],
            "bools": [True, False],
            "dates": [datetime.datetime(2018, 1, 1), datetime.datetime(2021, 1, 1)],
        }
    )

    assert schema.schema_from_dataframe(df) == {
        "numberRows": 2,
        "field": {
            "numbers": {"unique": 2, "dataType": "number"},
            "text": {"unique": 1, "dataType": "string"},
            "bools": {"unique": 2, "dataType": "boolean"},
            "dates": {"unique": 2, "dataType": "date"},
        },
    }


def test_load_unsupported_data():
    df = pd.DataFrame({"datetime": [pd.Timedelta("2 days")]})
    with pytest.raises(ValueError):
        schema.schema_from_dataframe(df)


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
    assert schema.file_to_facts(csv_file) == {
        "numberRows": 2,
        "field": {
            "numbers": {"unique": 2, "dataType": "number"},
            "text": {"unique": 1, "dataType": "string"},
        },
    }


@pytest.fixture(scope="session")
def json_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.json")
    with open(filename, "w") as f:
        json.dump([{"numbers": 1, "text": "a"}, {"numbers": 2, "text": "a"}], f)
    return str(filename)


def test_json_to_facts(json_file):
    assert schema.file_to_facts(json_file) == {
        "numberRows": 2,
        "field": {
            "numbers": {"unique": 2, "dataType": "number"},
            "text": {"unique": 1, "dataType": "string"},
        },
    }


def test_unknown_file_type():
    with pytest.raises(ValueError):
        schema.file_to_facts("foo.bar")
