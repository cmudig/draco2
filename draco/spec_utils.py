from typing import Iterable, Union

from draco.programs import constraints, definitions, hard, helpers
from draco.run import is_satisfiable


def check_spec(spec: Union[str, Iterable[str]]):
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
