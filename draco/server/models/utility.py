from typing import Mapping

from pydantic import BaseModel

from .shared import ClingoSymbol


class DictToFactsDTO(BaseModel):
    """Data Transfer Object to encode dictionaries as answer set programming facts"""

    data: Mapping | list | str


DictToFactsReturn = list[str]


class AnswerSetToDictDTO(BaseModel):
    """Data Transfer Object to decode an answer set into a nested data structure"""

    answer_set: list[ClingoSymbol] | list[str]


AnswerSetToDictReturn = Mapping
