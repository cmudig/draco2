from typing import Literal

# granular imports to satisfy `pyright`
import pydantic.class_validators as pydantic_validators
import pydantic.config as pydantic_config
import pydantic.fields as pydantic_fields
import pydantic.main as pydantic_main
import pydantic.types as pydantic_types

"""
The number of rows in the dataset.
"""
DatasetNumberRows = pydantic_types.PositiveInt

"""
ID set for a field to be used as the ``entity_id``
when being processed as an ASP entity.
"""
FieldId = str

"""
The name of a data field.
Described as `(field,name)`
"""
FieldName = str

"""
The type of the data in the column for this field.
One of number, string, boolean, or datetime.
Described as `(field,type)`
"""
FieldType = Literal["number", "string", "boolean", "datetime"]

"""
The number of unique values.
Described as `(field,unique)`
"""
FieldUnique = pydantic_types.PositiveInt

"""
The entropy of the field.
Described as `(field,entropy)`
"""
FieldEntropy = pydantic_types.PositiveFloat

"""
The minimum value. Only used for numbers.
Described as `(field,min)`
"""
FieldMin = float

"""
The maximum value. Only used for numbers.
Described as `(field,max)`
"""
FieldMax = float

"""
The standard deviation. Only used for numbers.
Described as `(field,std)`
"""
FieldStd = float

"""
The frequency of the most common value. Only used for strings.
Described as `(field,freq)`
"""
FieldFreq = pydantic_types.PositiveInt

"""
When the task regards specific fields, fields can be marked as relevant to the task.
Described as `(field,interesting)`
"""
FieldInteresting = bool

"""
The coordinates system of the view. Can be one of cartesian, or polar.
Described as `(view,coordinates)`.
"""
ViewCoordinate = Literal["cartesian", "polar"]

"""
The mark type. One of point, bar, line, area, text, tick, or rect.
Described as `(mark,type)`.
"""
MarkType = Literal["point", "bar", "line", "area", "text", "tick", "rect"]

"""
The visual channel. One of x, y, color, size, shape, or text.
Same as `ScaleChannel`.
Described as `(encoding,channel)`.
"""
EncodingChannel = Literal["x", "y", "color", "size", "shape", "text"]

"""
The field that maps to the visual property of the mark. Arbitrary string.
Described as `(encoding,field)`.
"""
EncodingField = FieldName

"""
How the data is aggregated. One of count, mean, median, min, max, stdev, or sum.
Described as `(encoding,aggregate)`.
"""
EncodingAggregate = Literal["count", "mean", "median", "min", "max", "stdev", "sum"]

"""
How the data is binned into N bins. Positive integer.
Described as `(encoding,binning)`
"""
EncodingBinning = pydantic_types.PositiveInt

"""
Stacking strategy. One of zero, center, or normalize.
Described as `(encoding,stack)`.
"""
EncodingStack = Literal["zero", "center", "normalize"]

"""
The scale channel. One of x, y, color, size, shape, or text.
Same as `EncodingChannel`.
Described as `(scale,channel)`.
"""
ScaleChannel = EncodingChannel

"""
The scale type. One of linear, log, ordinal, or categorical.
Described as `(scale,type)`.
"""
ScaleType = Literal["linear", "log", "ordinal", "categorical"]

"""
Whether to include zero in the scale domain.
Described as `(scale,zero)`.
"""
ScaleZero = bool

"""
The task type.
The task that the user tries to complete when looking at a visualization
helps Draco find the most appropriate visualization.
"""
Task = Literal["value", "summary"]

"""
The facet channel. Can be one of col and row.
Described as `(facet,channel)`.
"""
FacetChannel = Literal["col", "row"]

"""
The facet field. Arbitrary string.
Described as `(facet,field)`.
"""
FacetField = FieldName

"""
Binning a numeric field for faceting. Positive integer.
Described as `(facet,binning)`.
"""
FacetBinning = EncodingBinning


class SchemaBase(pydantic_main.BaseModel):
    """Base class for all schema classes."""

    class Config:
        # Do not allow fields that are not defined in the schema explicitly.
        extra = pydantic_config.Extra.forbid


class Encoding(SchemaBase):
    """
    Encoding schema.
    Encodings define how data fields map to visual properties (channel) of the mark.

    `Read More <https://dig.cmu.edu/draco2/facts/encoding.html>`__.
    """

    channel: EncodingChannel
    field: EncodingField | None = None
    aggregate: EncodingAggregate | None = None
    binning: EncodingBinning | None = None
    stack: EncodingStack | None = None

    @pydantic_validators.root_validator(pre=True)
    def check_field_is_present_unless_agg_count(cls, values: dict):
        if values.get("aggregate", None) != "count" and "field" not in values:
            raise ValueError("field must be present unless aggregate is count")
        return values


class Mark(SchemaBase):
    """
    Mark schema.
    A mark represents the graphical mark of the visualization.

    `Read More <https://dig.cmu.edu/draco2/facts/mark.html>`__.
    """

    type: MarkType
    encoding: list[Encoding]


class Scale(SchemaBase):
    """
    Scale schema.
    Scales map abstract values such as time or temperature to
    a visual value such as x- or y-position or color.

    `Read More <https://dig.cmu.edu/draco2/facts/scale.html>`__.
    """

    channel: ScaleChannel
    type: ScaleType = pydantic_fields.Field(default="linear")
    zero: ScaleZero | None = None


class Facet(SchemaBase):
    """
    Facet schema.
    With the facet operator, we can partition a dataset by a field
    and create a view for each field.
    The resulting chart is often called a small multiples chart.

    `Read More <https://dig.cmu.edu/draco2/facts/facet.html>`__.
    """

    channel: FacetChannel
    field: FacetField
    binning: FacetBinning | None = None


class View(SchemaBase):
    """
    View schema.
    A view can group marks and scales together.

    `Read More <https://dig.cmu.edu/draco2/facts/view.html>`__.
    """

    coordinates: ViewCoordinate = pydantic_fields.Field(default="cartesian")
    mark: list[Mark]
    facet: list[Facet] | None = None

    """
    View-specific scales define scales on a per-channel basis in the view.
    `None` means that a top-level scale (shared scale) is present.
    """
    scale: list[Scale] | None = None

    __SUPPORTED_POLAR_MARKS__ = {"bar"}
    __SUPPORTED_POLAR_ENCODINGS__ = {"x", "y", "color"}

    @pydantic_validators.root_validator(pre=True)
    def check_polar_mark_and_encoding(cls, values: dict):
        if values.get("coordinates", "cartesian") == "polar":
            for mark in values.get("mark", []):
                if mark.get("type", None) not in cls.__SUPPORTED_POLAR_MARKS__:
                    raise ValueError(
                        f"polar coordinates only support "
                        f"{cls.__SUPPORTED_POLAR_MARKS__} marks"
                    )
                for encoding in mark.get("encoding", []):
                    if (
                        encoding.get("channel", None)
                        not in cls.__SUPPORTED_POLAR_ENCODINGS__
                    ):
                        raise ValueError(
                            f"polar coordinates only support "
                            f"{cls.__SUPPORTED_POLAR_ENCODINGS__} encodings"
                        )
        return values


class Field(SchemaBase):
    """
    Field schema.
    Represents a column in the dataset.
    Draco can use information about the field type and field statistics.

    `Read More <https://dig.cmu.edu/draco2/facts/schema.html#field-properties>`__.
    """

    id: FieldId | None = pydantic_fields.Field(default=None, alias="__id__")
    name: FieldName
    type: FieldType
    unique: FieldUnique | None = None
    entropy: FieldEntropy | None = None
    min: FieldMin | None = None
    max: FieldMax | None = None
    std: FieldStd | None = None
    freq: FieldFreq | None = None
    interesting: FieldInteresting | None = None

    __STRING_ONLY_FIELDS__ = {"freq"}
    __NUMBER_ONLY_FIELDS__ = {"min", "max", "std"}

    @pydantic_validators.root_validator(pre=True)
    def check_no_string_attributes_on_number_type(cls, values: dict):
        if values["type"] == "number":
            for field in cls.__STRING_ONLY_FIELDS__:
                if field in values:
                    raise ValueError(
                        f"{field} is not a valid attribute for a number field"
                    )
        return values

    @pydantic_validators.root_validator(pre=True)
    def check_no_number_attributes_on_string_type(cls, values: dict):
        if values["type"] == "string":
            for field in cls.__NUMBER_ONLY_FIELDS__:
                if field in values:
                    raise ValueError(
                        f"{field} is not a valid attribute for a string field"
                    )
        return values


class SpecificationDict(SchemaBase):
    """
    Specification schema.
    Describes a visualization completely.
    """

    number_rows: DatasetNumberRows
    task: Task | None = None
    field: list[Field]
    view: list[View]

    """
    Top-level scales define shared scales across views.
    `None` means no shared scales are used.
    """
    scale: list[Scale] | None = None
