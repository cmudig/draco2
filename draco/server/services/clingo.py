from typing import Iterable

import draco.server.models.clingo as endpoint_models
from draco.run import run_clingo as run_clingo_internal
from draco.server.utils import model_to_jsonable_model


def run_clingo(
    program: str | Iterable[str], models: int, topK: bool, arguments: list[str]
) -> endpoint_models.RunClingoReturn:
    generator = run_clingo_internal(program, models, topK, arguments)
    return list(map(model_to_jsonable_model, generator))
