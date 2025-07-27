import csv
import datetime
import json
from pathlib import Path

import narwhals as nw
import pandas as pd
import pytest

from draco import schema

SIMPLE_SCHEMA = {
    "number_rows": 2,
    "field": [
        {
            "name": "numbers",
            "type": "number",
            "unique": 2,
            "max": 2,
            "min": 1,
            "std": 0,
            "skew": 0,
            "entropy": 693,
        },
        {"name": "text", "type": "string", "unique": 1, "freq": 2, "entropy": 0},
    ],
}


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
        "number_rows": 2,
        "field": [
            {
                "name": "numbers",
                "type": "number",
                "unique": 2,
                "max": 2,
                "min": 1,
                "std": 0,
                "skew": 0,
                "entropy": 693,
            },
            {"name": "text", "type": "string", "unique": 1, "freq": 2, "entropy": 0},
            {"name": "bools", "type": "boolean", "unique": 2, "entropy": 693},
            {"name": "dates", "type": "datetime", "unique": 2, "entropy": 693},
        ],
    }


def test_load_unsupported_data():
    # We don't support structs
    df = pd.DataFrame([{"x": 1}])
    with pytest.raises(ValueError):
        schema.schema_from_dataframe(df)


@pytest.mark.parametrize(
    "dtype,expected",
    [
        # Numeric types
        (nw.dtypes.Int8(), "number"),
        (nw.dtypes.Int16(), "number"),
        (nw.dtypes.Int32(), "number"),
        (nw.dtypes.Int64(), "number"),
        (nw.dtypes.UInt8(), "number"),
        (nw.dtypes.UInt16(), "number"),
        (nw.dtypes.UInt32(), "number"),
        (nw.dtypes.UInt64(), "number"),
        (nw.dtypes.Float32(), "number"),
        (nw.dtypes.Float64(), "number"),
        # Boolean type
        (nw.dtypes.Boolean(), "boolean"),
        # String type
        (nw.dtypes.String(), "string"),
        # Temporal types
        (nw.dtypes.Date(), "datetime"),
        (nw.dtypes.Datetime(), "datetime"),
        (nw.dtypes.Duration(), "datetime"),
    ],
)
def test_dtype_to_field_type(dtype: nw.dtypes.DType, expected: schema.FieldType):
    result = schema.dtype_to_field_type(dtype)
    assert result == expected


def test_dtype_to_field_type_unsupported():
    # Using List type as an example of unsupported type
    unsupported_dtype = nw.dtypes.List(nw.dtypes.String())
    with pytest.raises(ValueError, match="unsupported type"):
        schema.dtype_to_field_type(unsupported_dtype)


@pytest.fixture(scope="session")
def csv_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.csv")
    headers = ["numbers", "text"]
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow({"numbers": 1, "text": "a"})
        writer.writerow({"numbers": 2, "text": "a"})
    return Path(filename)


def test_csv_to_schema(csv_file):
    assert schema.schema_from_file(csv_file) == SIMPLE_SCHEMA


@pytest.fixture(scope="session")
def json_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.json")
    with open(filename, "w") as f:
        json.dump([{"numbers": 1, "text": "a"}, {"numbers": 2, "text": "a"}], f)
    return Path(filename)


def test_json_to_schema(json_file):
    assert schema.schema_from_file(json_file) == SIMPLE_SCHEMA


def test_unknown_file_type():
    with pytest.raises(ValueError):
        schema.schema_from_file(Path("foo.bar"))
