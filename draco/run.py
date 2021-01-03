"""
Run constraint solver to complete spec.
"""

import json
import logging
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Union

import clyngor
from clyngor.answers import Answers
from pprint import pprint

from draco.utils import asp_to_vl


DEBUG = True

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

# --- Logic Programming Constraints --- #
# [*] define.lp: declares the domains to visualization attributes and defines useful helper functions.
#   You almost definitely want this file.
# [*] generate.lp: describe the candidate solution (i.e. search space)
# [*] hard.lp: restricts the search space to only well-formed and expressive specifications.
# soft.lp: defines soft constraints in the form of violation/1 and violation/2 predicates.
#   By themselves, these predicates don't change the search.
# weights.lp: declares default (hand tuned) weights similar to those in CompassQL.
#   There is one constant for each rule in soft.lp. We use this file to generate assign_weights.lp.
# assign_weights.lp: uses violation_weight/2 to assign every violation predicate a weight.
#   These weights usually come from weights.lp. This file is generated from weights.lp.
# optmize.lp: defined the minimization function.
# [*] output.lp: declares which predicates should be shown when an answer set is printed.

DRACO_LP = [
    "define.lp",
    "generate.lp",
    "hard.lp",
    "hard-integrity.lp",
    # "soft.lp",
    # "weights.lp",
    # "assign_weights.lp",
    # "optimize.lp",
    "output.lp",
]
DRACO_LP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../asp")


file_cache: Dict[str, bytes] = {}


class Result:
    props: List[str]
    cost: Optional[int]
    violations: Dict[str, int]

    def __init__(self, answers: Answers, cost: Optional[int] = None) -> None:
        violations: Dict[str, int] = defaultdict(int)
        props: List[str] = []

        for ((head, body),) in answers:
            if head == "cost":
                cost = int(body[0])
            elif head == "soft":
                violations[body[0]] += 1
            else:
                b = ",".join(map(str, body))
                props.append(f"{head}({b}).")

        self.props = props
        self.violations = violations
        self.cost = cost

    def as_vl(self) -> Dict:
        return asp_to_vl(self.props)


def load_file(path: str) -> bytes:
    content = file_cache.get(path)
    if content is not None:
        return content
    with open(path, encoding="utf-8") as f:
        content = f.read().encode("utf8")
        file_cache[path] = content
        return content


def run_clingo(
    draco_query: List[str],
    constants: Dict[str, str] = None,
    files: List[str] = None,
    relax_hard=False,
    silence_warnings=False,
    debug=False,
    multiple_solution=False,
) -> Tuple[bytes, bytes]:
    """
    Run draco and return stderr and stdout
    """

    # default args
    files = files or DRACO_LP
    if relax_hard and "hard-integrity.lp" in files:
        files.remove("hard-integrity.lp")

    constants = constants or {}

    options = ["--outf=2", "--models=0"]
    if multiple_solution:
        # print all solutions
        options += ["--quiet=0,2,2"]
    else:
        # only print the optimal solution
        options += ["--quiet=1,2,2"]

    if silence_warnings:
        options.append("--warn=no-atom-undefined")
    for name, value in constants.items():
        options.append(f"-c {name}={value}")

    cmd = ["clingo"] + options
    if DEBUG:
        logger.debug("Command: %s", " ".join(cmd))

    proc = subprocess.Popen(
        args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    program = "\n".join(draco_query)

    file_names = [os.path.join(DRACO_LP_DIR, f) for f in files]
    asp_program = b"\n".join(map(load_file, file_names)) + program.encode("utf8")
    if debug:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fd:
            fd.write(program)
            if DEBUG:
                logger.info(
                    'Debug ASP with "clingo %s %s"', " ".join(file_names), fd.name
                )

    stdout, stderr = proc.communicate(asp_program)

    return (stderr, stdout)


def run(
    draco_query: List[str],
    constants: Dict[str, str] = None,
    files: List[str] = None,
    relax_hard=False,
    silence_warnings=False,
    debug=False,
    clear_cache=False,
    multiple_solution=False,
):
    """ Run clingo to compute a completion of a partial spec or violations. """

    # Clear file cache. useful during development in notebooks.
    if clear_cache and file_cache:
        logger.warning("Cleared file cache")
        file_cache.clear()

    stderr, stdout = run_clingo(
        draco_query,
        constants,
        files,
        relax_hard,
        silence_warnings,
        debug,
        multiple_solution,
    )

    try:
        json_result = json.loads(stdout)
    except json.JSONDecodeError:
        logger.error("stdout: %s", stdout)
        logger.error("stderr: %s", stderr)
        raise

    if stderr:
        logger.error(stderr)

    result = json_result["Result"]

    if result == "UNSATISFIABLE":
        # print(f'{result}')
        if DEBUG:
            print("unsat")
            print(json.loads(stdout))
            logger.info("Constraints are unsatisfiable.")
        return None
    elif result == "OPTIMUM FOUND":
        # get the last witness, which is the best result
        all_answers = json_result["Call"][0]["Witnesses"]

        for answers in all_answers:
            if DEBUG:
                logger.debug(answers["Value"])

        results = [
            Result(
                clyngor.Answers(answers["Value"]).sorted,
                cost=json_result["Models"]["Costs"][0],
            )
            for answers in all_answers
        ]

        # print(f'{result} | {json_result["Models"]["Costs"][0]} | {len(results)}')

        if multiple_solution:
            return results
        else:
            return results[-1]
    elif result == "SATISFIABLE":
        all_answers = json_result["Call"][0]["Witnesses"]

        # print(f'{result} | {json_result["Models"]["Number"]}')

        # assert (
        #     json_result["Models"]["Number"] > 1
        # ), "Should not have more than one model if we don't optimize"

        if DEBUG:
            for answers in all_answers:
                logger.debug(answers["Value"])
        return [
            Result(
                clyngor.Answers(answers["Value"]).sorted,
                cost=-1,
            )
            for answers in all_answers
        ]
    else:
        logger.error("Unsupported result: %s", result)
        return None
