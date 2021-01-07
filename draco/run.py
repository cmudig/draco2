from collections import namedtuple
from typing import Iterable, Union

import clingo

Model = namedtuple("Model", ["answer_set", "cost", "number"])


def run_clingo(program: Union[str, Iterable[str]] = "", models: int = 0):
    """
    Run the solver. Returns all models by default.
    """
    if not isinstance(program, str):
        program = "\n".join(program)

    ctl = clingo.Control()
    ctl.add(
        "base",
        [],
        program,
    )
    ctl.ground([("base", [])])

    if models is not None:
        ctl.configuration.solve.models = str(models)

    ctl.configuration.solve.project = 1

    with ctl.solve(yield_=True) as handle:
        for model in handle:
            answer_set = model.symbols(shown=True)
            yield Model(answer_set, model.cost, model.number)
