import clingo

from draco.run import Model

from .models.shared import ClingoModel, ClingoSymbol


def clingo_symbol_to_jsonable_symbol(symbol: clingo.Symbol) -> ClingoSymbol:
    return {"type": symbol.type.name, "value": str(symbol)}


def model_to_jsonable_model(model: Model) -> ClingoModel:
    return {
        "cost": model.cost,
        "number": model.number,
        "answer_set": list(map(clingo_symbol_to_jsonable_symbol, model.answer_set)),
    }
