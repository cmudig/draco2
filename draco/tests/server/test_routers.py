from typing import Any, Type

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import draco.server.routers as routers
from draco import Draco
from draco.fact_utils import dict_to_facts
from draco.server import DracoAPI


@pytest.fixture
def default_draco() -> Draco:
    return Draco()


@pytest.fixture
def draco_api(default_draco: Draco) -> DracoAPI:
    return DracoAPI(default_draco)


@pytest.fixture
def app(draco_api: DracoAPI) -> FastAPI:
    return draco_api.app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize(
    "cls",
    [
        routers.DracoRouter,
        routers.UtilityRouter,
        routers.DracoRouter,
    ],
)
def test_init_router(default_draco: Draco, cls: Type[routers.BaseDracoRouter]):
    router = cls(default_draco)
    assert router is not None


@pytest.mark.parametrize(
    "cls",
    [
        routers.DracoRouter,
        routers.UtilityRouter,
        routers.DracoRouter,
    ],
)
def test_register_router(default_draco: Draco, cls: Type[routers.BaseDracoRouter]):
    router = cls(default_draco)
    assert router is not None

    # Precondition
    assert len(router.routes) == 0
    router.register()
    # Precondition
    assert len(router.routes) > 0


@pytest.mark.parametrize(
    "json",
    [
        {"program": "fact(a,42)."},
        {"program": "fact(a,42).", "models": 0, "topK": False, "arguments": []},
        {
            "program": "2 { a(1..5) }. :- not a(2). #minimize { 1,X : a(X) }.",
            "models": 10,
            "topK": True,
        },
    ],
)
def test_clingo_run(client: TestClient, json: dict[str, Any]):
    response = client.post("/clingo/run", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {"spec": dict_to_facts({"mark": [{"type": "point"}]})},
    ],
)
def test_draco_check_spec(client: TestClient, json: dict[str, Any]):
    response = client.post("/draco/check-spec", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {
            "spec": dict_to_facts({"mark": [{"type": "point"}]}),
            "models": 1,
        }
    ],
)
def test_draco_complete_spec(client: TestClient, json: dict[str, Any]):
    response = client.post("/draco/complete-spec", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [{"spec": dict_to_facts({"mark": [{"type": "point"}]})}],
)
def test_draco_count_preferences(client: TestClient, json: dict[str, Any]):
    response = client.post("/draco/count-preferences", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {"spec": dict_to_facts({"mark": [{"type": "point"}]})},
    ],
)
def test_draco_get_violations(client: TestClient, json: dict[str, Any]):
    response = client.post("/draco/get-violations", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {"data": {"zero": False}},
        {"data": {"zero": True}},
        {
            "data": {
                "numberRows": 42,
                "field": [
                    {
                        "type": "number",
                        "bin": [{"maxbins": 20}],
                    },
                ],
            },
        },
    ],
)
def test_utility_dict_to_facts(client: TestClient, json: dict[str, Any]):
    response = client.post("/utility/dict-to-facts", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {
            "answer_set": [
                # root
                "attribute(numberRows,root,42).",
                # first field
                "entity(field,root,0).",
                "attribute((field,type),0,number).",
                "entity(bin,0,1).",
                "attribute((bin,maxbins),1,20).",
            ]
        },
        {
            "answer_set": [
                {"type": "Function", "value": "entity(view,root,0)"},
                {"type": "Function", "value": "entity(mark,0,1)"},
                {"type": "Function", "value": "attribute((mark,type),1,bar)"},
                {"type": "Function", "value": "entity(encoding,1,2)"},
                {"type": "Function", "value": "attribute((encoding,channel),2,x)"},
                {"type": "Function", "value": "attribute((encoding,field),2,foo)"},
                {"type": "Function", "value": "entity(scale,0,3)"},
                {"type": "Function", "value": "attribute((scale,channel),3,x)"},
                {"type": "Function", "value": "attribute((scale,type),3,linear)"},
            ]
        },
    ],
)
def test_utility_answer_set_to_dict(client: TestClient, json: dict[str, Any]):
    response = client.post("/utility/answer-set-to-dict", json=json)
    assert response.ok
