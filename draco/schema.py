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
        return "datetime"
    else:
        raise ValueError(f"unsupported type {ty}")


def schema_from_dataframe(
    df: pd.DataFrame, parse_data_type=dtype_to_field_type
) -> Dict:
    """
    Read schema information from the given Pandas dataframe.
    """
    schema: Dict[str, Any] = {}

    schema["numberRows"] = df.shape[0]
    schema["field"] = {}

    for col in df.columns:
        column = df[col]
        dtype = column.dtype
        unique = pd.Series.nunique(column)
        data_type = parse_data_type(dtype)

        props = {"dataType": data_type, "unique": unique}

        if data_type == "number":
            props["min"] = int(column.min())
            props["max"] = int(column.max())
            props["std"] = int(column.std())

        elif data_type == "string":
            objcounts = column.value_counts()
            props["freq"] = objcounts.iloc[0]

        schema["field"][col] = props

    return schema


def file_to_facts(file: str, parse_data_type=dtype_to_field_type) -> Dict:
    """
    Read schema information from the given CSV or JSON file.
    """
    if file.endswith(".json"):
        df: Any = pd.read_json(file)
        return schema_from_dataframe(df, parse_data_type)
    elif file.endswith(".csv"):
        df = pd.read_csv(file)
        return schema_from_dataframe(df, parse_data_type)
    else:
        raise ValueError(f"unsupported file type {file}")
