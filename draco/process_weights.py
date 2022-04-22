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


def get_weights_assigned(weight_path: Path, assign_path: Path) -> WeightsAssign:
    """Reads the weights file and generates assign_weights.lp"""
    with open(weight_path) as weight_constants:
        const_prog = weight_constants.read()
        const_dict = get_constants(const_prog)
        assign_prog = "%% GENERATED FILE. DO NOT EDIT.\n"

        for name in const_dict:
            match = re.search("(.*)_weight", name)
            if match:
                assign_prog += f"preference_weight({match.group(1)},{name}).\n"

    with open(assign_path, "w") as assign:
        assign.write(assign_prog)

    return WeightsAssign(const_prog, assign_prog, const_dict)


def set_new_weights(
    curr_weights: WeightsAssign,
    new_weights: Dict[str, int],
    weight_path: Path = asp_path / "weights.lp",
    assign_path: Path = asp_path / "assign_weights.lp",
) -> WeightsAssign:
    """Overwrite the weight values
    and add new weights if they didn't exist before.
    The weights and assign_weights files will also be updated.
    """
    weights = curr_weights.weights
    assign_prog = curr_weights.assign_program

    for name in new_weights:
        if name not in weights:
            match = re.search("(.*)_weight", name)
            if match:
                assign_prog += f"preference_weight({match.group(1)},{name}).\n"

        weights[name] = new_weights[name]

    weights_prog = ""
    for name in weights:
        weights_prog += f"#const {name} = {weights[name]}.\n"

    with open(weight_path, "w") as weights_file, open(assign_path, "w") as assign_file:
        weights_file.write(weights_prog)
        assign_file.write(assign_prog)

    return WeightsAssign(weights_prog, assign_prog, weights)


weights = get_weights_assigned(asp_path / "weights.lp", asp_path / "assign_weights.lp")
