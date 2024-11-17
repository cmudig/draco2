from typing import Mapping

import pytest

import draco.server.services.clingo as clingo_service
import draco.server.services.renderer as renderer_service
import draco.server.services.utility as utility_service
import draco.types as draco_types
from draco import Draco
from draco.run import run_clingo
from draco.server.services.draco import DracoService


@pytest.fixture
def default_draco() -> Draco:
    return Draco()


@pytest.fixture
def default_draco_service(default_draco: Draco) -> DracoService:
    return DracoService(default_draco)


def test_run_clingo():
    res = clingo_service.run_clingo("fact(a,42).", models=1, topK=False, arguments=[])
    expected = list(run_clingo("fact(a,42).", models=0, topK=False, arguments=[]))
    assert res is not None
    assert len(res) == len(expected)
    for res_item, expected_item in zip(res, expected):
        assert res_item["cost"] == expected_item.cost
        assert res_item["number"] == expected_item.number
        for res_answer, expected_answer in zip(
            res_item["answer_set"], expected_item.answer_set
        ):
            assert res_answer["type"] == expected_answer.type.name
            assert res_answer["value"] == str(expected_answer)


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
def test_check_spec(
    spec: draco_types.Specification,
    default_draco: Draco,
    default_draco_service: DracoService,
):
    service = default_draco_service
    res = service.check_spec(spec)
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
def test_complete_spec(
    spec: draco_types.Specification, default_draco_service: DracoService
):
    service = default_draco_service
    num_models = 10
    res = service.complete_spec(spec, num_models)
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
def test_count_preferences(
    spec: draco_types.Specification,
    default_draco: Draco,
    default_draco_service: DracoService,
):
    service = default_draco_service
    res = service.count_preferences(spec)
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
def test_get_violations(
    spec: draco_types.Specification,
    default_draco: Draco,
    default_draco_service: DracoService,
):
    service = default_draco_service
    res = service.get_violations(spec)
    assert res is not None
    assert res == default_draco.get_violations(spec)


@pytest.mark.parametrize(
    "inp,expected",
    [
        ({"zero": False}, [":- attribute(zero,root)."]),
        ({"zero": True}, ["attribute(zero,root)."]),
        (
            {
                "numberRows": 42,
                "field": [
                    {
                        "type": "number",
                        "bin": [{"maxbins": 20}],
                    },
                ],
            },
            [
                # root
                "attribute(numberRows,root,42).",
                # first field
                "entity(field,root,0).",
                "attribute((field,type),0,number).",
                "entity(bin,0,1).",
                "attribute((bin,maxbins),1,20).",
            ],
        ),
        (
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "bar",
                                "encoding": [{"channel": "x", "field": "foo"}],
                            }
                        ],
                        "scale": [{"channel": "x", "type": "linear"}],
                    }
                ],
            },
            [
                "entity(view,root,0).",
                "entity(mark,0,1).",
                "attribute((mark,type),1,bar).",
                "entity(encoding,1,2).",
                "attribute((encoding,channel),2,x).",
                "attribute((encoding,field),2,foo).",
                "entity(scale,0,3).",
                "attribute((scale,channel),3,x).",
                "attribute((scale,type),3,linear).",
            ],
        ),
    ],
)
def test_dict_to_facts(inp: Mapping | list | str, expected: list[str]):
    res = utility_service.dict_to_facts(data=inp)
    assert res is not None
    assert res == expected


@pytest.mark.parametrize(
    "expected,inp",
    [
        (
            {
                "numberRows": 42,
                "field": [
                    {
                        "type": "number",
                        "bin": [{"maxbins": 20}],
                    },
                ],
            },
            [
                # root
                "attribute(numberRows,root,42).",
                # first field
                "entity(field,root,0).",
                "attribute((field,type),0,number).",
                "entity(bin,0,1).",
                "attribute((bin,maxbins),1,20).",
            ],
        ),
        (
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "bar",
                                "encoding": [{"channel": "x", "field": "foo"}],
                            }
                        ],
                        "scale": [{"channel": "x", "type": "linear"}],
                    }
                ],
            },
            [
                "entity(view,root,0).",
                "entity(mark,0,1).",
                "attribute((mark,type),1,bar).",
                "entity(encoding,1,2).",
                "attribute((encoding,channel),2,x).",
                "attribute((encoding,field),2,foo).",
                "entity(scale,0,3).",
                "attribute((scale,channel),3,x).",
                "attribute((scale,type),3,linear).",
            ],
        ),
        (
            {
                "view": [
                    {
                        "mark": [
                            {
                                "type": "bar",
                                "encoding": [{"channel": "x", "field": "foo"}],
                            }
                        ],
                        "scale": [{"channel": "x", "type": "linear"}],
                    }
                ],
            },
            [
                {"type": "Function", "value": "entity(view,root,0)"},
                {"type": "Function", "value": "entity(mark,0,1)"},
                {"type": "Function", "value": "attribute((mark,type),1,bar)"},
                {"type": "Function", "value": "entity(encoding,1,2)"},
                {"type": "Function", "value": "attribute((encoding,channel),2,x)"},
                {"type": "Function", "value": "attribute((encoding,field),2,foo)"},
                {"type": "Function", "value": "entity(scale,0,3)"},
                {"type": "Function", "value": "attribute((scale,channel),3,x)"},
                {"type": "Function", "value": "attribute((scale,type),3,linear)"},
            ],
        ),
    ],
)
def test_answer_set_to_dict(inp: list[str], expected: Mapping):
    res = utility_service.answer_set_to_dict(answer_set=inp)
    assert res is not None
    assert res == expected


@pytest.mark.parametrize(
    "spec",
    [
        {
            "number_rows": 42,
            "field": [
                {
                    "name": "a",
                    "type": "number",
                },
                {
                    "name": "b",
                    "type": "number",
                },
            ],
            "view": [
                {
                    "coordinates": "cartesian",
                    "mark": [
                        {
                            "type": "bar",
                            "encoding": [
                                {
                                    "channel": "x",
                                    "field": "a",
                                },
                                {
                                    "channel": "y",
                                    "field": "b",
                                },
                            ],
                        }
                    ],
                    "scale": [
                        {"channel": "x", "type": "ordinal"},
                        {"channel": "y", "type": "linear", "zero": "true"},
                    ],
                }
            ],
        }
    ],
)
def test_render_spec(spec: dict):
    vl_chart = renderer_service.render_spec(spec)
    assert isinstance(vl_chart, dict)
