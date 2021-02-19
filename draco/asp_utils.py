import re
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, TextIO, Union


@dataclass
class Block:
    """Class for a code block."""

    # The type of code block.
    block_type: str

    # Short description of the code block.
    description: str

    # The program in Answer Set Programming (ASP).
    program: str


METADATA_PREFIX = "% @"

Blocks = Dict[Optional[str], Union[Block, str]]


def parse_blocks(program: Union[str, Path]) -> Blocks:
    if isinstance(program, Path):
        with open(program) as f:
            return _parse_blocks(f)
    else:
        return _parse_blocks(StringIO(program))


def _parse_blocks(f: TextIO) -> Blocks:
    """
    Parses definitions, constraints, or other blocks from ASP files.
    In an ASP file, a block is denoted with a comment of the form:

    ```
    # %foo(name) description
    ```
    """
    defs: Blocks = {}

    # find the first block
    line = f.readline()
    preamble = [line]
    while not line.startswith(METADATA_PREFIX) and len(line):
        line = f.readline()
        if not line.startswith(METADATA_PREFIX) and len(line.strip()):
            preamble.append(line)

    if len([line for line in preamble if line.strip()]):
        defs["__preamble__"] = "".join(preamble).lstrip()

    # exit if we have reached the end of the file already
    if len(line) == 0:
        return defs

    # read the blocks one by one
    while True:
        block = [line]

        line = f.readline()
        block.append(line)

        while len(line):
            line = f.readline()

            if line.startswith(METADATA_PREFIX):
                break
            elif len(line.strip()):
                block.append(line)

        match = re.match(rf"{METADATA_PREFIX}(\w+)\((\w+)\) ([^\n]+)", block[0])

        if match:
            block_type, name, description = match.groups()
            defs[name] = Block(block_type, description, "".join(block[1:]))

        if len(line) == 0:
            return defs


def blocks_to_program(blocks: Blocks) -> List[str]:
    return [b.program for b in blocks.values() if isinstance(b, Block)]
