from typing import Any, DefaultDict, Dict, Generator, List, Optional

import draco.server.models as models
from draco import Draco
from draco.run import Model


def draco_from_payload(payload: models.DracoInitDTO) -> Draco:
    return Draco(**payload.dict())


def get_properties(
    names: List[models.DracoProperty], draco: Draco
) -> Dict[models.DracoProperty, Any]:
    return {name: getattr(draco, name) for name in names}


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
