from dataclasses import dataclass
from typing import Any, Iterable, List, Union

import clingo


@dataclass
class Model:
    """Class for a model."""

    # The answer set of this model.
    answer_set: List[clingo.Symbol]

    # The cost of this answer set.
    cost: int

    # The sequence number of this answer.
    number: int


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

    config: Any = ctl.configuration

    if models is not None:
        config.solve.models = str(models)

    config.solve.project = 1

    solve_handle = ctl.solve(yield_=True)
    if isinstance(solve_handle, clingo.solving.SolveHandle):
        with solve_handle as handle:
            for model in handle:
                answer_set = model.symbols(shown=True)
                yield Model(answer_set, model.cost, model.number)


def is_satisfiable(program: Union[str, Iterable[str]] = ""):
    try:
        next(run_clingo(program, 1))
        return True
    except StopIteration:
        return False
