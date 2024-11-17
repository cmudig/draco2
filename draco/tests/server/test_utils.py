from fastapi import FastAPI

import draco.server.utils as server_utils


def test_tabulate_routes():
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}  # pragma: no cover

    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: str | None = None):
        return {"item_id": item_id, "q": q}  # pragma: no cover

    output = server_utils.tabulate_routes(app)

    assert "read_root" in output
    assert "/" in output
    assert "GET" in output
    assert "read_item" in output
    assert "/items/{item_id}" in output
    assert "GET" in output
