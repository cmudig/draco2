import logging
from dataclasses import dataclass
from typing import Any, Generator, Iterable, List, Sequence, Tuple, Union, cast

# Clingo Python API is documented at https://potassco.org/clingo/python-api/current/
import clingo


@dataclass(frozen=True)
class Model:
    """Class for a model.

    Attributes:
        :answer_set: The answer set of this model.
            An answer set is a list of Clingo Symbols.
        :cost: The cost of this answer set.
        :number: The sequence number of this answer.
    """

    answer_set: Iterable[clingo.Symbol]
    cost: List[int]
    number: int

    def __str__(self):
        return "\n".join([f"{s}." for s in self.answer_set])


class Observer(clingo.backend.Observer):
    def __init__(self):
        self.minimize_literals: Sequence[Tuple[int, int]] = []

    def minimize(self, priority: int, literals: Sequence[Tuple[int, int]]):
        self.minimize_literals = literals


def run_clingo(
    program: Union[str, Iterable[str]],
    models: int = 0,
    topK=False,
    arguments: List[str] = [],
) -> Generator[Model, None, None]:
    """Run the solver and yield the models.

    :param program: Program as a string or iterable of strings that will be
        concatenated.
    :param models: Number of models to generate, defaults to 0 (meaning all models).
    :param topK: Whether to return the top K models. If false (default), the program
        will not optimize the output models.
    :param arguments: Arguments to the clingo grounder and solver.
        Only gringo options (without --text) and clasp's search options are supported.
        For example, you can use ["-c foo=5"] to override the occurrences of
        constant "foo" in your input program.
        Refer to the potassco guide for the options.
    :yield: The models.
    """
    if not isinstance(program, str):
        program = "\n".join(program)

    # single-shot solving is often faster, but we cannot change the program
    ctl = clingo.Control(["--single-shot"] + arguments if not topK else arguments)
    config: Any = ctl.configuration

    ctl.add(
        "base",
        [],
        program,
    )

    # topK with all models is the same as ignoring optimization
    if topK and models == 0:
        logging.warning("Since all models should be computed, topK is ignored.")
        topK = False
        config.solve.opt_mode = "ignore"

    if topK:
        config.solve.opt_mode = "optN"
        config.solve.quiet = 1

        obs = Observer()
        ctl.register_observer(obs)

        ctl.ground([("base", [])])

        while models > 0:
            cost = 0
            config.solve.models = str(models)

            solve_handle = cast(clingo.solving.SolveHandle, ctl.solve(yield_=True))
            with solve_handle as handle:
                for model in handle:
                    if model.optimality_proven:
                        cost = model.cost[0]
                        models -= 1

                        answer_set = model.symbols(shown=True)
                        yield Model(answer_set, model.cost, model.number)
                if handle.get().unsatisfiable:
                    break

            if models > 0:
                # add weight rule to disallow optimal models in next solve call
                with ctl.backend() as backend:
                    aux = backend.add_atom()
                    backend.add_weight_rule([aux], cost + 1, obs.minimize_literals)
                    backend.add_rule([], [-aux])

    else:
        config.solve.models = str(models)

        config.solve.project = 1

        ctl.ground([("base", [])])

        solve_handle = cast(clingo.solving.SolveHandle, ctl.solve(yield_=True))
        with solve_handle as handle:
            for model in handle:
                answer_set = model.symbols(shown=True)
                yield Model(answer_set, model.cost, model.number)


def is_satisfiable(program: Union[str, Iterable[str]]) -> bool:
    """Checks whether the program is satisfiable.

    :param program: Program as a string or iterable of strings that will be
        concatenated.
    :return: Whether the program is satisfiable.
    """
    try:
        next(run_clingo(program, 1))
        return True
    except StopIteration:
        return False
