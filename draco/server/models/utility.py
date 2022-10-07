from typing import Mapping

from pydantic import BaseModel

from draco.fact_utils import ROOT

from .shared import ClingoSymbol


class DictToFactsDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to encode dictionaries as answer set programming facts"""

    data: Mapping | list | str
    path: list = []
    parent: str | int = ROOT


DictToFactsReturn = list[str]


class AnswerSetToDictDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to decode an answer set into a nested data structure"""

    answer_set: list[ClingoSymbol]
    root: str | int = ROOT


AnswerSetToDictReturn = Mapping
