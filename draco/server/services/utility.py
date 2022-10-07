from typing import Mapping

import draco.fact_utils as fact_utils
import draco.server.models.utility as endpoint_models
from draco.server.models.shared import ClingoSymbol


def dict_to_facts(
    data: Mapping | list | str, path: list, parent: str | int
) -> endpoint_models.DictToFactsReturn:
    return fact_utils.dict_to_facts(data, tuple(path), parent)


def answer_set_to_dict(
    answer_set: list[ClingoSymbol], root: str | int
) -> endpoint_models.AnswerSetToDictReturn:
    # return fact_utils.answer_set_to_dict(answer_set, root)
    return {}
