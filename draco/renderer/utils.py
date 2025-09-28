from .altair.types import (
    EncodingChannel,
    Field,
    FieldName,
    FieldType,
    Scale,
    SpecificationDict,
    View,
)
from .base_renderer import LabelMapping


def find_encoding_channel_of_field(
    views: list[View], field_name: FieldName
) -> EncodingChannel | None:
    """
    Returns the mark encoding channel for the field with the given name.

    :param views: All the views in the spec to search for.
    :param field_name: The name of the field to search for.
    :return: The encoding channel of the field, or `None` if
             the field is not found.
    """
    for v in views:
        for m in v.mark:
            for e in m.encoding:
                if e.field == field_name:
                    return e.channel

    return None


def find_scales_of_spec(spec: SpecificationDict) -> list[Scale]:
    """
    Returns all the scales in the spec including the top-level
    shared scale and the view-specific scales.

    :param spec: The spec to search through for scales.
    :return: A list of all the scales in the spec.
    """
    scales: list[Scale] = []

    # Shared scales
    for s in spec.scale or []:
        scales.append(s)

    # View-specific scales
    for v in spec.view:
        for s in v.scale or []:
            scales.append(s)

    return scales


def find_field_by_name(fields: list[Field], field_name: FieldName) -> Field:
    """
    Returns the field with the given name.

    :param fields: The list of fields to search through.
    :param field_name: The name of the field to search for.
    :return: The field with the given name.
    :raises ValueError: If the field is not found.
    """
    for f in fields:
        if f.name == field_name:
            return f

    raise ValueError(f"Field {field_name} not found")


def find_scale_for_encoding(
    channel: EncodingChannel, scales: list[Scale]
) -> Scale | None:
    """
    Returns the `Scale` for the given encoding channel, if any.

    :param channel: the channel for which to look up a scale
    :param scales: the list of scales in the view
    :return: the scale for the given channel, or None if no scale is found
    """
    for scale in scales:
        if scale.channel == channel:
            return scale
    return None


def find_raw_field_type(fields: list[Field], field_name: FieldName | None) -> FieldType:
    if field_name is None:
        return "number"

    field_type = find_field_by_name(fields, field_name)
    return field_type.type


def resolve_label(label_mapping: LabelMapping, field_name: FieldName) -> str:
    if isinstance(label_mapping, dict):
        return label_mapping.get(field_name, field_name)
    return label_mapping(field_name)
