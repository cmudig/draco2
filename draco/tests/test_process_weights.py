from pathlib import Path

import pytest

from draco.process_weights import get_weights_assigned, set_new_weights, weights


def test_has_weights():
    assert len(weights.weights_program)
    assert len(weights.assign_program)
    assert len(weights.weights)


WEIGHTS = """

#const preference1_weight = 1.
#const preference2_weight = 2.
#const preference3_weight = 3.

"""


@pytest.fixture(scope="session")
def weight_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test_weights.asp")
    with open(filename, "w") as f:
        f.write(WEIGHTS)
    return Path(filename)


@pytest.fixture(scope="session")
def assign_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test_assign.asp")
    return Path(filename)


@pytest.fixture(scope="session")
def write_weights_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("write_weights.asp")
    return Path(filename)


@pytest.fixture(scope="session")
def write_assign_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("write_assign.asp")
    return Path(filename)


def test_set_new_weights(
    weight_file, assign_file, write_weights_file, write_assign_file
):
    weights = get_weights_assigned(weight_file, assign_file)
    new_weights = set_new_weights(
        weights,
        {"preference1_weight": 100, "new_weight": 4},
        write_weights_file,
        write_assign_file,
    )

    assert new_weights.weights == {
        "preference1_weight": 100,
        "preference2_weight": 2,
        "preference3_weight": 3,
        "new_weight": 4,
    }

    assert (
        new_weights.assign_program
        == weights.assign_program + "preference_weight(new,new_weight).\n"
    )

    with open(write_weights_file) as write_weights, open(
        write_assign_file
    ) as write_assign:
        assert write_weights.read() == new_weights.weights_program
        assert write_assign.read() == new_weights.assign_program
