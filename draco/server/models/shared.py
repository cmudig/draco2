from typing_extensions import TypedDict


class ClingoSymbol(TypedDict):
    """JSON-serializable clingo symbol"""

    type: str
    value: str


class ClingoModel(TypedDict):
    """JSON-serializable clingo model"""

    answer_set: list[ClingoSymbol]
    cost: list[int]
    number: int
