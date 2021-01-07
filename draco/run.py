from typing import Iterable, Union

import clingo


def run_clingo(program: Union[str, Iterable[str]] = "", models: int = None):
    """
    Run the solver.
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
        for m in handle:
            # print(f"Type: {m.type}")
            print(f"Number: {m.number}")
            # print(f"Optimal: {m.optimality_proven}")
            # print(f"Cost: {m.cost}")
            print(f"Atoms: {m.symbols(atoms=True)}")
            # print(f"Answer: {m}")
            print()
