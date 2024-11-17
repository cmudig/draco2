import clingo
from fastapi import FastAPI
from fastapi.routing import APIRoute
from tabulate import tabulate

from draco.run import Model

from .models.shared import ClingoModel, ClingoSymbol


def clingo_symbol_to_jsonable_symbol(symbol: clingo.Symbol) -> ClingoSymbol:
    return {"type": symbol.type.name, "value": str(symbol)}


def model_to_jsonable_model(model: Model) -> ClingoModel:
    return {
        "cost": model.cost,
        "number": model.number,
        "answer_set": list(map(clingo_symbol_to_jsonable_symbol, model.answer_set)),
    }


def tabulate_routes(app: FastAPI):
    """
    Tabulates the routes registered by the server.

    :return: a string containing the tabulated routes.
    """
    route_table_headers = ["Name", "Path", "Methods", "Tags"]
    route_table = [
        [
            route.name,
            route.path,
            ", ".join(route.methods),
            ", ".join(map(str, route.tags)),
        ]
        for route in app.routes
        # Only show the API routes, ignore swagger, redoc, etc. routes
        if isinstance(route, APIRoute)
    ]
    return tabulate(route_table, headers=route_table_headers, tablefmt="github")
