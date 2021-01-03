import pandas as pd
from draco import Fact, utils
import pytest
import csv


def test_load_df():
    df = pd.DataFrame([[1, "a"], [2, "a"]], columns=["numbers", "text"])
    assert sorted(utils.df_to_facts(df)) == sorted(
        [
            Fact("numberRows", 2),
            Fact("fieldCardinality", ("numbers", 2)),
            Fact("fieldCardinality", ("text", 1)),
            Fact("fieldDataType", ("numbers", "number")),
            Fact("fieldDataType", ("text", "string")),
        ]
    )


@pytest.fixture(scope="session")
def file_name(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.csv")
    headers = ["numbers", "text"]
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow({"numbers": 1, "text": "a"})
        writer.writerow({"numbers": 2, "text": "a"})
    return str(filename)


def test_csv_to_facts(file_name):
    assert sorted(utils.file_to_facts(file_name)) == sorted(
        [
            Fact("numberRows", 2),
            Fact("fieldCardinality", ("numbers", 2)),
            Fact("fieldCardinality", ("text", 1)),
            Fact("fieldDataType", ("numbers", "number")),
            Fact("fieldDataType", ("text", "string")),
        ]
    )
