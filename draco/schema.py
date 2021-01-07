from typing import Any, Dict

import pandas as pd


def dtype_to_field_type(ty):
    """
    Simple converter that translates Pandas column types to data types for Draco.
    """
    if ty in ["float64", "int64"]:
        return "number"
    elif ty in ["bool"]:
        return "boolean"
    elif ty in ["object"]:
        return "string"
    elif ty in ["datetime64[ns]"]:
        return "date"
    else:
        raise ValueError(f"unsupported type {ty}")


def schema_from_dataframe(
    df: pd.DataFrame, parse_data_type=dtype_to_field_type
) -> dict:
    """
    Read data statistics from the given dataframe.
    """

    schema: Dict[str, Any] = {}

    schema["numberRows"] = df.shape[0]

    schema["field"] = {}
    fields = schema["field"]

    for col in df.columns:
        unique = pd.Series.nunique(df[col])
        data_type = parse_data_type(df[col].dtype)

        fields[col] = {"unique": unique, "dataType": data_type}

    return schema


def file_to_facts(file: str, parse_data_type=dtype_to_field_type) -> dict:
    """
    Read data statistics from the given CSV or JSON file.
    """

    if file.endswith(".json"):
        df: Any = pd.read_json(file)
        return schema_from_dataframe(df, parse_data_type)
    elif file.endswith(".csv"):
        df = pd.read_csv(file)
        return schema_from_dataframe(df, parse_data_type)
    else:
        raise ValueError(f"unsupported file type {file}")
