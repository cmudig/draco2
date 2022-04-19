"""
Reads the weights file and generates assign_weights.lp and weights.json
"""

import re
from pathlib import Path

asp_path = Path(__file__).resolve().parent / "asp"


def main():
    with open(asp_path / "weights.lp") as weight_constants, open(
        asp_path / "assign_weights.lp", "w"
    ) as assign:

        assign.write("%% GENERATED FILE. DO NOT EDIT.\n\n")

        weights = {}

        for line in weight_constants.readlines():
            match = re.search("#const (.*)_weight = ([-0-9]*)", line)
            if match:
                name = match.group(1)
                value = int(match.group(2))

                weights[f"{name}_weight"] = value

                assign.write(f"preference_weight({name},{name}_weight).\n")


if __name__ == "__main__":
    main()
