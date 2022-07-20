from collections import defaultdict
from typing import DefaultDict, Iterable, Union

import draco.programs as programs
from draco.asp_utils import blocks_to_program, parse_blocks
from draco.run import is_satisfiable, run_clingo
from draco.weights import Weights, assign_program
from draco.weights import weights as draco_weights

Program = programs.Program


class Draco:
    """A class for holding all the programs used by Draco."""

    def __init__(
        self,
        define: Union[Program, str] = programs.define,
        constraints: Union[Program, str] = programs.constraints,
        helpers: Union[Program, str] = programs.helpers,
        generate: Union[Program, str] = programs.generate,
        hard: Union[Program, str] = programs.hard,
        soft: Union[Program, str] = programs.soft,
        optimize: Union[Program, str] = programs.optimize,
        weights: Union[Weights, dict] = draco_weights,
    ):
        """Create a Draco helper class. If no programs are passed in, the default
        Draco programs are used.

        Parameters:
            :param define: The program for defining variables.
            :param constraints: The program for defining constraints.
            :param helpers: The program for defining helper functions.
            :param generate: The program for generating facts.
            :param hard: The program for defining hard constraints.
            :param soft: The program for defining soft constraints.
            :param optimize: The program for optimizing soft constraints.
            :param weights: The program for assigning weights to soft
                constraints.
            :param soft_constraint_names: The names of the soft constraints
                which can be used as features for ML.
        """

        def to_string(prog: Union[Program, str]):
            if isinstance(prog, Program):
                return prog.program
            else:
                return prog

        self.define = to_string(define)
        self.constraints = to_string(constraints)
        self.helpers = to_string(helpers)
        self.generate = to_string(generate)
        self.hard = to_string(hard)
        self.soft = to_string(soft)
        self.optimize = to_string(optimize)
        self.weights = weights.weights if isinstance(weights, Weights) else weights

        constraints_blocks = (
            constraints.blocks
            if isinstance(constraints, Program)
            else parse_blocks(constraints)
        )
        self._constraints_no_violation = "".join(
            blocks_to_program(
                constraints_blocks, set(constraints_blocks.keys()) - set(["violation"])
            )
        )

        self.assign_weights = (
            weights.assign_program
            if isinstance(weights, Weights)
            else assign_program(weights)
        )

        self.soft_constraint_names = sorted(
            [s[: -len("_weight")] for s in self.weights.keys()]
        )

        if isinstance(soft, Program) and weights is not None:
            soft_constraints = set(soft.blocks.keys())
            soft_constraints.remove("__preamble__")
            weight_keys = set(self.soft_constraint_names)

            assert (
                soft_constraints == weight_keys
            ), "Weights dictionary does not match soft constraints"

    def check_spec(self, spec: Union[str, Iterable[str]]) -> bool:
        """Checks the spec against the hard constraints.

        Internally, Draco checks against the definitions, constraints, helpers,
        and hard constraints.

        :param spec: The specification to check
        """
        if not isinstance(spec, str):
            spec = "\n".join(spec)

        program = self.define + self.constraints + self.helpers + self.hard + spec
        return is_satisfiable(program)

    def complete_spec(self, spec: Union[str, Iterable[str]], models=1):
        """Get optimal completions for the [partial input specification.

        :param spec: The partial specification to complete.
        :param models: The number of completetions to return, defaults to 1
        """
        if not isinstance(spec, str):
            spec = "\n".join(spec)

        program = (
            self.define
            + self.generate
            + self.constraints
            + self.helpers
            + self.hard
            + self.soft
            + self.assign_weights
            + self.optimize
            + spec
        )

        # pass the weights as constraint to Clingo
        args = [f"-c {w}={v}" for w, v in self.weights.items()]

        return run_clingo(program, models, True, args)

    def count_preferences(self, spec: Union[str, Iterable[str]]):
        """Get a dictionary from preferences to how often a given specification
        violates the preference. Returns None if the problem is not satisfiable.

        Internally, Draco checks against the definitions, constraints, helpers,
        and soft constraints.

        :param spec: The specification to check
        """
        if not isinstance(spec, str):
            spec = "\n".join(spec)

        program = self.define + self.constraints + self.helpers + self.soft + spec

        try:
            result: DefaultDict[str, int] = defaultdict(int)

            model = next(run_clingo(program, 1))

            for symbol in model.answer_set:
                if symbol.name == "preference":
                    result[symbol.arguments[0].name] += 1

            return result
        except StopIteration:
            return None

    def get_violations(self, spec: Union[str, Iterable[str]]):
        """Get the list of violations for a given specification. Returns None if the
        problem is not satisfiable.

        Internally, Draco checks against the definitions, constraints (without the
        constraint that disallows violations), helpers, and hard constraints.

        :param spec: The specification to check
        """
        if not isinstance(spec, str):
            spec = "\n".join(spec)

        program = (
            self.define
            + self._constraints_no_violation
            + self.helpers
            + self.hard
            + spec
        )

        try:
            model = next(run_clingo(program, 1))

            return [
                symbol.arguments[0].name
                for symbol in model.answer_set
                if symbol.name == "violation"
            ]
        except StopIteration:
            # Since the problem is not satisfiable, we return None to distinguish it
            # from satisfiable programs where you would expect violations to be []
            return None
