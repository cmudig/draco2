from pathlib import Path

import pytest

from draco.process_weights import get_weights_assigned, weights


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


def test_get_weights(weight_file):
    weights = get_weights_assigned(weight_file)

    assert weights.weights == {
        "preference1_weight": 1,
        "preference2_weight": 2,
        "preference3_weight": 3,
    }
