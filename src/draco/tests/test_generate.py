from pathlib import Path

from draco import run_clingo
from draco.asp_utils import get_constants
from draco.programs import constraints, define, generate, hard, helpers

asp_path = Path(__file__).resolve().parent.parent / "asp"


def test_generate():
    prog = (
        generate.program
        + define.program
        + helpers.program
        + hard.program
        + constraints.program
    )
    with open(asp_path / "examples" / "scatter.lp") as file:
        scatter = file.read()

    models = list(
        run_clingo(
            prog + scatter + ":- {entity(mark,_,_)} < 3.", 10, False, ["-c max_marks=3"]
        )
    )

    assert len(models) > 0


def test_generate_const():
    program = generate.program

    assert get_constants(program) == {"max_views": 1, "max_marks": 2, "max_encs": 4}
