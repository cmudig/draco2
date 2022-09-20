import clingo
import pytest

import draco.server.models as models
import draco.server.utils as utils
from draco.run import Model


@pytest.mark.parametrize(
    "inp,expected", [(clingo.Number(10), {"type": "Number", "value": "10"})]
)
def test_symbol_to_json(inp: clingo.Symbol, expected: models.ClingoSymbol):
    res = utils.clingo_symbol_to_jsonable_symbol(inp)
    assert res == expected


@pytest.mark.parametrize(
    "inp,expected",
    [
        (
            Model(answer_set=[], cost=[0], number=1),
            {"answer_set": [], "cost": [0], "number": 1},
        ),
        (
            Model(answer_set=[clingo.Number(10)], cost=[0], number=1),
            {
                "answer_set": [{"type": "Number", "value": "10"}],
                "cost": [0],
                "number": 1,
            },
        ),
    ],
)
def test_model_to_json(
    inp: Model,
    expected: models.ClingoModel,
):
    res = utils.model_to_jsonable_model(inp)
    assert res == expected
