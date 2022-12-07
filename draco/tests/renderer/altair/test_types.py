import pytest

import draco.renderer.altair.types as draco_types


@pytest.mark.parametrize(
    "data, is_valid",
    [
        (dict(channel="x", field="temp"), True),
        (dict(channel="x", field="temp", aggregate="mean"), True),
        (dict(channel="x", field="temp", aggregate="count"), True),
        (dict(channel="x", aggregate="count"), True),
        (dict(channel="x", aggregate="mean"), False),
    ],
)
def test_encoding_validator(data: dict, is_valid: bool):
    if is_valid:
        draco_types.Encoding(**data)
    else:
        with pytest.raises(ValueError):
            draco_types.Encoding(**data)


@pytest.mark.parametrize(
    "data, is_valid",
    [
        (dict(name="temp", type="number"), True),
        (dict(name="temp", type="number", min=-20, max=50, std=0), True),
        (dict(name="temp", type="number", min=-20, max=50, std=0, freq=100), False),
        (dict(name="temp", type="string", min=-20, max=50, std=0), False),
    ],
)
def test_field_validator(data: dict, is_valid: bool):
    if is_valid:
        draco_types.Field(**data)
    else:
        with pytest.raises(ValueError):
            draco_types.Field(**data)


@pytest.mark.parametrize(
    "data, is_valid",
    [
        # Cartesian - valid
        *[
            (
                dict(
                    coordinates="cartesian",
                    mark=[dict(type=t, encoding=[dict(channel="x", field="temp")])],
                ),
                True,
            )
            for t in ["point", "bar", "line", "area", "text", "tick", "rect"]
        ],
        # Polar - invalid mark, valid encoding
        *[
            (
                dict(
                    coordinates="polar",
                    mark=[dict(type=t, encoding=[dict(channel="x", field="temp")])],
                ),
                False,
            )
            for t in ["point", "line", "area", "text", "tick", "rect"]
        ],
        # Polar - valid mark, valid encoding
        *[
            (
                dict(
                    coordinates="polar",
                    mark=[dict(type=t, encoding=[dict(channel="x", field="temp")])],
                ),
                True,
            )
            for t in ["bar"]
        ],
        # Polar - valid mark, invalid encoding
        *[
            (
                dict(
                    coordinates="polar",
                    mark=[dict(type="bar", encoding=[dict(channel=c, field="temp")])],
                ),
                False,
            )
            for c in ["size", "shape", "text"]
        ],
        # Polar - valid mark, valid encoding
        *[
            (
                dict(
                    coordinates="polar",
                    mark=[dict(type="bar", encoding=[dict(channel=c, field="temp")])],
                ),
                True,
            )
            for c in ["x", "y", "color"]
        ],
    ],
)
def test_view_validator(data: dict, is_valid: bool):
    if is_valid:
        draco_types.View(**data)
    else:
        with pytest.raises(ValueError):
            draco_types.View(**data)
