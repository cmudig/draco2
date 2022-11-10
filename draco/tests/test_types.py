import pytest

import draco.types as draco_types


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
