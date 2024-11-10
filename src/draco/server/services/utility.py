from typing import Mapping

from clingo import parse_term

import draco.fact_utils as fact_utils
import draco.server.models.utility as endpoint_models
from draco.server.models.shared import ClingoSymbol


def dict_to_facts(data: Mapping | list | str) -> endpoint_models.DictToFactsReturn:
    return fact_utils.dict_to_facts(data)


def answer_set_to_dict(
    answer_set: list[ClingoSymbol] | list[str],
) -> endpoint_models.AnswerSetToDictReturn:
    def c(value: str) -> str:
        """Removes trailing period from value"""
        if value.endswith("."):
            return value[:-1]
        return value

    # Convert JSON-friendly input to clingo symbols
    if isinstance(answer_set[0], str):
        str_answer_set: list[str] = answer_set  # type: ignore
        symbols = [parse_term(c(s)) for s in str_answer_set]
    else:
        symbol_answer_set: list[ClingoSymbol] = answer_set  # type: ignore
        symbols = [parse_term(c(s["value"])) for s in symbol_answer_set]

    return fact_utils.answer_set_to_dict(symbols)
