import re
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Optional, TextIO, Union

from clingo.ast import AST, ASTType, parse_string


@dataclass(frozen=True)
class Block:
    """Class for a code block.

    Attributes:
        :block_type: The type of code block.
        :description: Short description of the code block.
        :program: The program in Answer Set Programming (ASP).
    """

    block_type: str
    description: str
    program: str


METADATA_PREFIX = "% @"

Blocks = Dict[Optional[str], Union[Block, str]]


def parse_blocks(program: Union[str, Path]) -> Blocks:
    """Parses definitions, constraints, or other blocks from ASP files.
    In an ASP file, a block is denoted with a comment of the form:

    ```
    # %foo(name) description
    ```
    """
    if isinstance(program, Path):
        with open(program) as f:
            return _parse_blocks(f)
    else:
        return _parse_blocks(StringIO(program))


def _parse_blocks(f: TextIO) -> Blocks:
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


def blocks_to_program(
    blocks: Blocks, keys: Optional[Iterable[Union[str, None]]] = None
) -> List[str]:
    return [
        block.program
        for name, block in blocks.items()
        if isinstance(block, Block) and (keys is None or name in keys)
    ]


def get_constants(program: Union[str, Iterable[str]]) -> Dict:
    if isinstance(program, str):
        program = program.split("\n")

    constants = {}
    for line in program:

        def record(ast: AST):
            if ast.ast_type == ASTType.Definition:
                constants[ast.name] = int(str(ast.value))

        parse_string(line, lambda x: record(x))

    return constants
