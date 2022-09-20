from typing import Any, Dict, Optional

import pytest
from fastapi.testclient import TestClient

from draco.fact_utils import dict_to_facts
from draco.server.controller import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize(
    "json",
    [
        None,
        {"payload": {"names": []}},
        {"payload": {"names": ["define", "constraints", "helpers"]}},
    ],
)
def test_get_properties_existing(client: TestClient, json: Optional[Dict[str, Any]]):
    response = client.post("/properties", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {"payload": {"spec": dict_to_facts({"mark": [{"type": "point"}]})}},
    ],
)
def test_check_spec(client: TestClient, json: Dict[str, Any]):
    response = client.post("/check-spec", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {
            "payload": {
                "spec": dict_to_facts({"mark": [{"type": "point"}]}),
                "models": 1,
            }
        },
    ],
)
def test_complete_spec(client: TestClient, json: Dict[str, Any]):
    response = client.post("/complete-spec", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {"payload": {"spec": dict_to_facts({"mark": [{"type": "point"}]})}},
    ],
)
def test_count_preferences(client: TestClient, json: Dict[str, Any]):
    response = client.post("/count-preferences", json=json)
    assert response.ok


@pytest.mark.parametrize(
    "json",
    [
        {"payload": {"spec": dict_to_facts({"mark": [{"type": "point"}]})}},
    ],
)
def test_get_violations(client: TestClient, json: Dict[str, Any]):
    response = client.post("/get-violations", json=json)
    assert response.ok


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
def test_run_clingo(client: TestClient, json: Dict[str, Any]):
    response = client.post("/run-clingo", json=json)
    assert response.ok
