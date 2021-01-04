from typing import Any, List

import pandas as pd

from draco import Fact


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
    else:
        raise ValueError(f"unsupported type {ty}")


def df_to_facts(df: pd.DataFrame, parse_data_type=dtype_to_field_type) -> List[Fact]:
    """
    Read data statistics from the given dataframe.
    """

    facts = []
    facts.append(Fact("numberRows", df.shape[0]))

    for col in df.columns:
        cardinality = pd.Series.nunique(df[col])
        data_type = parse_data_type(df[col].dtype)

        facts.append(Fact("fieldCardinality", (col, cardinality)))
        facts.append(Fact("fieldDataType", (col, data_type)))

    return facts


def file_to_facts(file: str, parse_data_type=dtype_to_field_type) -> List[Fact]:
    """
    Read data statistics from the given CSV or JSON file.
    """

    if file.endswith(".json"):
        df: Any = pd.read_json(file)
        return df_to_facts(df, parse_data_type)
    elif file.endswith(".csv"):
        df = pd.read_csv(file)
        return df_to_facts(df, parse_data_type)
    else:
        raise ValueError(f"unsupported file type {file}")
