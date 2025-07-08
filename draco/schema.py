from math import e
from pathlib import Path
from typing import Callable, Literal, TypeAlias, TypedDict

import narwhals as nw
import numpy as np
import pandas as pd
from narwhals.typing import IntoDataFrame

# Field types recognized by a Draco schema.
FieldType: TypeAlias = Literal["number", "string", "boolean", "datetime"]


class BaseFieldProps(TypedDict):
    """Properties shared by fields of all types in a `Schema`."""

    name: str
    type: FieldType
    unique: int
    entropy: float


class NumberFieldProps(BaseFieldProps):
    """Properties of a `number` field in a `Schema`."""

    min: int
    max: int
    std: int


class StringFieldProps(BaseFieldProps):
    """Properties of a `string` field in a `Schema`."""

    freq: int


# Union of supported field properties.
FieldProps = NumberFieldProps | StringFieldProps | BaseFieldProps


class Schema(TypedDict):
    """Representation of a data schema including data and field properties."""

    number_rows: int
    field: list[FieldProps]


def dtype_to_field_type(ty: nw.dtypes.DType) -> FieldType:
    """Simple converter that translates Pandas column types to data types for Draco."""
    if ty.is_numeric():
        return "number"
    elif isinstance(ty, nw.dtypes.Boolean):
        return "boolean"
    elif isinstance(ty, nw.dtypes.String):
        return "string"
    elif ty.is_temporal():
        return "datetime"
    else:
        raise ValueError(f"unsupported type {ty}")


def schema_from_dataframe(
    df: IntoDataFrame,
    parse_data_type=dtype_to_field_type,
) -> Schema:
    """Read schema information from the given Pandas dataframe.

    :param df: DataFrame to generate schema for.
    :param parse_data_type: Function to parse data types.
    :return: A dictionary representing the schema.
    """
    nw_df = nw.from_native(df, eager_only=True)
    schema: Schema = {"number_rows": nw_df.shape[0], "field": []}

    for col in nw_df.columns:
        column = nw_df.get_column(col)
        props: FieldProps = _construct_field_props(column, parse_data_type)
        schema["field"].append(props)

    return schema


def _construct_field_props(
    column: nw.Series,
    parse_data_type: Callable[[nw.dtypes.DType], FieldType],
) -> FieldProps:
    """Construct a `FieldProps` object from a `DataFrame` column."""
    name = str(column.name)
    dtype = column.dtype
    unique = column.unique().len()
    data_type = parse_data_type(dtype)

    vc = column.value_counts(normalize=True, sort=False).get_column("proportion")
    entropy = -(vc * np.log(vc) / np.log(e)).sum()
    entropy = round(entropy * 1000)

    if data_type == "number":
        return NumberFieldProps(
            name=name,
            type=data_type,
            unique=unique,
            entropy=entropy,
            min=int(column.min()),
            max=int(column.max()),
            std=int(column.std()),
        )
    elif data_type == "string":
        objcounts = column.value_counts()
        return StringFieldProps(
            name=name,
            type=data_type,
            unique=unique,
            entropy=entropy,
            freq=objcounts.get_column("count").max(),
        )

    return BaseFieldProps(name=name, type=data_type, unique=unique, entropy=entropy)


def schema_from_file(file_path: Path, parse_data_type=dtype_to_field_type) -> Schema:
    """Read schema information from the given CSV or JSON file.

    :param file_path: Path to CSV or JSON file.
    :param parse_data_type: Function to parse data types.
    :raises ValueError: If the file has an unsupported data type.
    :return: A dictionary representing the schema.
    """
    if file_path.suffix == ".json":
        df = pd.read_json(str(file_path))
        return schema_from_dataframe(df, parse_data_type)
    elif file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
        return schema_from_dataframe(df, parse_data_type)
    else:
        raise ValueError(f"unsupported file type {file_path}")
