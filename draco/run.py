from typing import List, Tuple

import clingo


def run(program: str = "", facts: List[Tuple] = [], models: int = None):
    """
    Run the solver.
    """

    program = program or ""

    for fact in facts:
        fact_strings = map(str, fact)
        program += "fact({}).\n".format(",".join(fact_strings))

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
