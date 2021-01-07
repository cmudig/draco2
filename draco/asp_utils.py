import re
from collections import namedtuple

Block = namedtuple("Block", ["block_type", "description", "program"])


def parse_blocks(filename: str):
    """
    Parses definitions, constraints, or other blocks from ASP files.
    In an ASP file, a block is denoted with a comment of the form:

    ```
    # %foo(name) description
    ```
    """
    defs = {}

    with open(filename) as f:
        # find the first block
        line = f.readline()
        while not line.startswith("% @") and len(line):
            line = f.readline()

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

                if line.startswith("% @"):
                    break
                elif len(line.strip()):
                    block.append(line)

            match = re.match(r"% @(\w+)\((\w+)\) ([^\n]+)", block[0])

            if match:
                block_type, name, description = match.groups()
                defs[name] = Block(block_type, description, "".join(block[1:]))

            if len(line) == 0:
                return defs
