from typing import Iterable

from pydantic import BaseModel

from .shared import ClingoModel


class RunClingoDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to run clingo via ``draco.run.run_clingo``."""

    program: str | Iterable[str]
    models: int = 0
    topK: bool = False
    arguments: list[str] = []


RunClingoReturn = list[ClingoModel]
