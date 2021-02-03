from pathlib import Path

from draco.asp_utils import parse_blocks

asp_path = Path(__file__).resolve().parent / "asp"

definitions = parse_blocks(asp_path / "define.lp")
constraints = parse_blocks(asp_path / "constraints.lp")
generate = parse_blocks(asp_path / "generate.lp")
