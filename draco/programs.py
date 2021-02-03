from dataclasses import dataclass
from pathlib import Path

from draco.asp_utils import Blocks, parse_blocks

asp_path = Path(__file__).resolve().parent / "asp"


@dataclass
class Program:
    program: str
    blocks: Blocks


def get_program(file_path: Path) -> Program:
    with open(file_path) as f:
        prog = f.read()
        return Program(prog, parse_blocks(prog))


definitions = get_program(asp_path / "define.lp")
constraints = get_program(asp_path / "constraints.lp")
generate = get_program(asp_path / "generate.lp")
