from typing import List, Union

import pytest

import draco.programs as programs
import draco.server.exceptions as exceptions
import draco.server.models as models
import draco.server.service as service
from draco import Draco
from draco.run import run_clingo
from draco.weights import Weights

Program = programs.Program


@pytest.fixture
def default_draco() -> Draco:
    return Draco()


@pytest.mark.parametrize(
    "payload",
    [
        models.DracoInitDTO(),
        models.DracoInitDTO(define="define"),
        models.DracoInitDTO(constraints="constraints"),
    ],
)
def test_draco_from_payload(payload: models.DracoInitDTO):
    draco = service.draco_from_payload(payload)
    assert draco is not None

    def to_string(prog: Union[Program, str]):
        if isinstance(prog, Program):
            return prog.program
        else:
            return prog

    assert draco.define == to_string(payload.define)
    assert draco.constraints == to_string(payload.constraints)
    assert draco.helpers == to_string(payload.helpers)
    assert draco.generate == to_string(payload.generate)
    assert draco.hard == to_string(payload.hard)
    assert draco.soft == to_string(payload.soft)
    assert draco.optimize == to_string(payload.optimize)
    assert (
        draco.weights == payload.weights.weights
        if isinstance(payload.weights, Weights)
        else payload.weights
    )


@pytest.mark.parametrize("names", [[], ["define"], ["define", "constraints"]])
def test_get_properties(names: List[models.DracoProperty], default_draco: Draco):
    prop_dict = service.get_properties(names, default_draco)
    assert prop_dict is not None
    assert len(prop_dict) == len(names)
    for name in names:
        assert name in prop_dict
        assert prop_dict[name] == default_draco.__dict__[name]


@pytest.mark.parametrize("names", [["x"], ["define", "x"], ["x", "y"]])
def test_get_properties_unknown_property(
    names: List[models.DracoProperty], default_draco: Draco
):
    with pytest.raises(exceptions.UnknownDracoPropertyError):
        service.get_properties(names, default_draco)


@pytest.mark.parametrize(
    "spec",
    [
        """
        attribute(number_rows,root,100).
        entity(field,root,temperature).
        """,
        ["attribute(number_rows,root,100).", "entity(field,root,temperature)."],
        ("attribute(number_rows,root,100).", "entity(field,root,temperature)."),
    ],
)
def test_check_spec(spec: models.Specification, default_draco: Draco):
    res = service.check_spec(spec, default_draco)
    assert res is not None
    assert res == default_draco.check_spec(spec)


@pytest.mark.parametrize(
    "spec",
    [
        """
        attribute(number_rows,root,100).
        entity(field,root,temperature).
        """,
        ["attribute(number_rows,root,100).", "entity(field,root,temperature)."],
        ("attribute(number_rows,root,100).", "entity(field,root,temperature)."),
    ],
)
def test_complete_spec(spec: models.Specification, default_draco: Draco):
    num_models = 10
    res = service.complete_spec(spec, num_models, default_draco)
    assert res is not None


@pytest.mark.parametrize(
    "spec",
    [
        """
        attribute(number_rows,root,100).
        entity(field,root,temperature).
        """,
        ["attribute(number_rows,root,100).", "entity(field,root,temperature)."],
        ("attribute(number_rows,root,100).", "entity(field,root,temperature)."),
    ],
)
def test_count_preferences(spec: models.Specification, default_draco: Draco):
    res = service.count_preferences(spec, default_draco)
    assert res is not None
    assert res == default_draco.count_preferences(spec)


@pytest.mark.parametrize(
    "spec",
    [
        """
        attribute(number_rows,root,100).
        entity(field,root,temperature).
        """,
        ["attribute(number_rows,root,100).", "entity(field,root,temperature)."],
        ("attribute(number_rows,root,100).", "entity(field,root,temperature)."),
    ],
)
def test_get_violations(spec: models.Specification, default_draco: Draco):
    res = service.get_violations(spec, default_draco)
    assert res is not None
    assert res == default_draco.get_violations(spec)


def test_run_clingo():
    res = list(
        service.run_clingo("fact(a,42).", num_models=0, topK=False, arguments=[])
    )
    expected = list(run_clingo("fact(a,42).", models=0, topK=False, arguments=[]))
    assert res is not None
    assert len(res) == len(expected)
    for res_item, expected_item in zip(res, expected):
        assert res_item.cost == expected_item.cost
        assert res_item.number == expected_item.number
        assert list(res_item.answer_set) == list(expected_item.answer_set)
