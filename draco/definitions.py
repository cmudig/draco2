import os

from draco.asp_utils import parse_blocks

definitions = parse_blocks(os.path.join(os.path.dirname(__file__), "asp/define.lp"))
