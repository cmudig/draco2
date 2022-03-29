from dataclasses import dataclass
from pathlib import Path

from draco.asp_utils import Blocks, parse_blocks

asp_path = Path(__file__).resolve().parent / "asp"


@dataclass(frozen=True)
class Program:
    """Class for an Answer Set Programming (ASP) program.

    Attributes:
        :program: The complete program.
        :blocks: The blocks in the program.
    """

    program: str
    blocks: Blocks


def get_program(file_path: Path) -> Program:
    with open(file_path) as f:
        prog = f.read()
        return Program(prog, parse_blocks(prog))


define = get_program(asp_path / "define.lp")
constraints = get_program(asp_path / "constraints.lp")
generate = get_program(asp_path / "generate.lp")
hard = get_program(asp_path / "hard.lp")
helpers = get_program(asp_path / "helpers.lp")
soft = get_program(asp_path / "soft.lp")
