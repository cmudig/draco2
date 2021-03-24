from dataclasses import dataclass
from typing import Any, Generator, Iterable, List, Union

import clingo


@dataclass
class Model:
    """Class for a model.

    Attributes:
        :answer_set: The answer set of this model.
            An answer set is a list of Clingo Symbols.
        :cost: The cost of this answer set.
        :number: The sequence number of this answer.
    """

    answer_set: List[clingo.Symbol]
    cost: int
    number: int


def run_clingo(
    program: Union[str, Iterable[str]], models: int = 0
) -> Generator[Model, None, None]:
    """Run the solver and yield the models.


    :param program: Program as a string or iterable of strings that will be
        concatenated.
    :param models: Number of models to generate, defaults to 0 (meaning all models)
    :yield: The models.
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


def is_satisfiable(program: Union[str, Iterable[str]]) -> bool:
    """Checks whether the program is satisfiable

    :param program: Program as a string or iterable of strings that will be
        concatenated.
    :return: Whether the program is satisfiable.
    """
    try:
        next(run_clingo(program, 1))
        return True
    except StopIteration:
        return False
