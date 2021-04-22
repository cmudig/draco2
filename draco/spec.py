from typing import Iterable, Union

from draco.asp_utils import blocks_to_program
from draco.programs import constraints, definitions, hard, helpers
from draco.run import is_satisfiable, run_clingo


def check_spec(spec: Union[str, Iterable[str]]) -> bool:
    """Checks the spec against the hard constraints.

    Internally, Draco checks against the definitions, constraints, helpers,
    and hard constraints.

    :param spec: The specification to check
    """
    if not isinstance(spec, str):
        spec = "\n".join(spec)

    program = (
        definitions.program
        + constraints.program
        + helpers.program
        + hard.program
        + spec
    )
    return is_satisfiable(program)


def get_violations(spec: Union[str, Iterable[str]]):
    """Get the list of violations for a given specification. Returns None if the
    problem is not satisfiable.

    Internally, Draco checks against the definitions, constraints, helpers,
    and hard constraints.

    :param spec: The specification top check
    """
    if not isinstance(spec, str):
        spec = "\n".join(spec)

    c = "".join(
        blocks_to_program(
            constraints.blocks, set(constraints.blocks.keys()) - set(["violation"])
        )
    )

    program = definitions.program + c + helpers.program + hard.program + spec

    try:
        model = next(run_clingo(program, 1))

        return [
            symbol.arguments[0].name
            for symbol in model.answer_set
            if symbol.name == "violation"
        ]
    except StopIteration:
        # Since the problem is not satisfiable, we return None to distinguish it from
        # satisfiable programs where you would expect violations to be []
        return None
