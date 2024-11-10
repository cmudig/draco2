import logging
from pathlib import Path

import pytest

from draco.programs import soft
from draco.weights import read_weights, weights


def test_has_weights():
    assert len(weights.assign_program)
    assert len(weights.weights)


WEIGHTS = """

#const preference1_weight = 1.
#const preference2_weight = 2.
#const preference3_weight = 3.

"""

INVALID = """

#const preference1 = 1.

"""


@pytest.fixture(scope="session")
def weight_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test_weights.asp")
    with open(filename, "w") as f:
        f.write(WEIGHTS)
    return Path(filename)


@pytest.fixture(scope="session")
def invalid_name_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("invalid.asp")
    with open(filename, "w") as f:
        f.write(INVALID)
    return Path(filename)


def test_get_weights(weight_file):
    weights = read_weights(weight_file)

    assert weights.weights == {
        "preference1_weight": 1,
        "preference2_weight": 2,
        "preference3_weight": 3,
    }


def test_invalid_name(invalid_name_file, caplog):
    with caplog.at_level(logging.WARNING):
        read_weights(invalid_name_file)
    assert (
        'Constant "preference1" doesn\'t end with "_weight", so it\'s not assigned.'
        in caplog.text
    )


def test_complete_weights():
    soft_constraints = set(soft.blocks.keys())
    soft_constraints.remove("__preamble__")

    weight_keys = {s[: -len("_weight")] for s in weights.weights.keys()}

    assert soft_constraints == weight_keys
