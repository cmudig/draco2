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


def read_program(file_path: Path) -> Program:
    with open(file_path) as f:
        prog = f.read()
        return Program(prog, parse_blocks(prog))


define = read_program(asp_path / "define.lp")
constraints = read_program(asp_path / "constraints.lp")
generate = read_program(asp_path / "generate.lp")
hard = read_program(asp_path / "hard.lp")
helpers = read_program(asp_path / "helpers.lp")
soft = read_program(asp_path / "soft.lp")
optimize = read_program(asp_path / "optimize.lp")
