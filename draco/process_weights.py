import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from draco.asp_utils import get_constants

asp_path = Path(__file__).resolve().parent / "asp"


@dataclass(frozen=True)
class WeightsAssign:
    """Class for weights and assigning weights in an Answer Set Programming (ASP) program.

    Attributes:
        :weights_program: The weights constants in the program.
        :assign_program: The weight assigning functions in the program.
        :weights: The weight constants as a dictionaty.
    """

    weights_program: str
    assign_program: str
    weights: Dict[str, int]


def get_weights_assigned(weight_path: Path) -> WeightsAssign:
    """Reads the weights file and assigns the weights to the preferences."""
    with open(weight_path) as weight_constants:
        const_prog = weight_constants.read()
        const_dict = get_constants(const_prog)
        assign_prog = ""

        for name in const_dict:
            match = re.search("(.*)_weight", name)
            if match:
                assign_prog += f"preference_weight({match.group(1)},{name}).\n"
            else:
                logging.warning(
                    f'Constant "{name}" doesn\'t end with "_weight", \
                        so it\'s not assigned.'
                )

    return WeightsAssign(const_prog, assign_prog, const_dict)


weights = get_weights_assigned(asp_path / "weights.lp")
