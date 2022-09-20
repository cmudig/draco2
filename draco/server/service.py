from typing import Any, DefaultDict, Dict, Generator, Iterable, List, Optional, Union

import draco.server.exceptions as exceptions
import draco.server.models as models
from draco import Draco
from draco.run import Model
from draco.run import run_clingo as run_clingo_internal


def draco_from_payload(payload: models.DracoInitDTO) -> Draco:
    return Draco(**payload.dict())


def get_properties(
    names: List[models.DracoProperty], draco: Draco
) -> Dict[models.DracoProperty, Any]:
    result = {}
    for name in names:
        try:
            result[name] = getattr(draco, name)
        except AttributeError:
            raise exceptions.UnknownDracoPropertyError(name)
    return result


def check_spec(spec: models.Specification, draco: Draco) -> bool:
    return draco.check_spec(spec)


def complete_spec(
    spec: models.Specification, num_models: int, draco: Draco
) -> Generator[Model, None, None]:
    return draco.complete_spec(spec, num_models)


def count_preferences(
    spec: models.Specification, draco: Draco
) -> Optional[DefaultDict[str, int]]:
    return draco.count_preferences(spec)


def get_violations(spec: models.Specification, draco: Draco) -> Optional[List[str]]:
    return draco.get_violations(spec)


def run_clingo(
    program: Union[str, Iterable[str]],
    num_models: int,
    topK,
    arguments: List[str],
):
    return run_clingo_internal(program, num_models, topK, arguments)
