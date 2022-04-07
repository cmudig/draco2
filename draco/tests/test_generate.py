from pathlib import Path

from draco import run_clingo
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
