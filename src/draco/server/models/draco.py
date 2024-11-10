from typing import DefaultDict

from pydantic import BaseModel

from draco.types import Specification

from .shared import ClingoModel


class CheckSpecDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to check a specification via ``Draco.check_spec``."""

    spec: Specification


CheckSpecReturn = bool


class CompleteSpecDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to complete a specification via ``Draco.complete_spec``."""

    spec: Specification
    models: int = 1


CompleteSpecReturn = list[ClingoModel]


class CountPreferencesDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to count preferences via ``Draco.count_preferences``."""

    spec: Specification


CountPreferencesReturn = DefaultDict[str, int] | None


class GetViolationsDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to get violations via ``Draco.get_violations``."""

    spec: Specification


GetViolationsReturn = list[str] | None
