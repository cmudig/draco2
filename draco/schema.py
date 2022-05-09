from math import e
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd


def dtype_to_field_type(ty):
    """Simple converter that translates Pandas column types to data types for
    Draco.
    """
    if ty in ["float64", "int64"]:
        return "number"
    elif ty in ["bool"]:
        return "boolean"
    elif ty in ["object"]:
        return "string"
    elif ty in ["datetime64[ns]"]:
        return "datetime"
    else:
        raise ValueError(f"unsupported type {ty}")


def schema_from_dataframe(
    df: pd.DataFrame, parse_data_type=dtype_to_field_type
) -> Dict[str, Any]:
    """Read schema information from the given Pandas dataframe.

    :param df: DataFrame to generate schema for.
    :param parse_data_type: Function to parse data types.
    :return: A dictionary representing the schema.
    """
    schema: Dict[str, Any] = {}

    schema["number_rows"] = df.shape[0]
    schema["field"] = []

    for col in df.columns:
        column = df[col]
        dtype = column.dtype
        unique = pd.Series.nunique(column)
        data_type = parse_data_type(dtype)

        vc = pd.Series(column).value_counts(normalize=True, sort=False)
        entropy = -(vc * np.log(vc) / np.log(e)).sum()
        entropy = round(entropy * 1000)

        props = {"name": col, "type": data_type, "unique": unique, "entropy": entropy}

        if data_type == "number":
            props["min"] = int(column.min())
            props["max"] = int(column.max())
            props["std"] = int(column.std())

        elif data_type == "string":
            objcounts = column.value_counts()
            props["freq"] = objcounts.iloc[0]

        schema["field"].append(props)

    return schema


def schema_from_file(
    file_path: Path, parse_data_type=dtype_to_field_type
) -> Dict[str, Any]:
    """Read schema information from the given CSV or JSON file.

    :param file_path: Path to CSV or JSON file.
    :param parse_data_type: Function to parse data types.
    :raises ValueError: If the file has an unsupported data type.
    :return: A dictionary representing the schema.
    """
    if file_path.suffix == ".json":
        df: Any = pd.read_json(str(file_path))
        return schema_from_dataframe(df, parse_data_type)
    elif file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
        return schema_from_dataframe(df, parse_data_type)
    else:
        raise ValueError(f"unsupported file type {file_path}")
