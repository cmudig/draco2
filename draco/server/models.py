from typing import Any, DefaultDict, Dict, Iterable, List, Literal, Optional, Union

from pydantic import BaseModel

import draco.programs as programs
from draco.run import Model
from draco.weights import Weights
from draco.weights import weights as draco_weights

Program = programs.Program

# Names of public props of a Draco instance
DracoProperty = Literal[
    "define",
    "constraints",
    "helpers",
    "generate",
    "hard",
    "soft",
    "optimize",
    "weights",
    "assign_weights",
    "soft_constraint_names",
]


class PropertyDTO(BaseModel):  # pytype: disable=base-class-error
    """
    Data Transfer Object to access public properties
    of a Draco instance via ``getattr``.
    """

    names: List[DracoProperty] = list(DracoProperty.__dict__["__args__"])


GetPropertiesReturn = Dict[DracoProperty, Any]


class DracoInitDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to construct a Draco instance via ``Draco.__init__``."""

    define: Union[Program, str] = programs.define
    constraints: Union[Program, str] = programs.constraints
    helpers: Union[Program, str] = programs.helpers
    generate: Union[Program, str] = programs.generate
    hard: Union[Program, str] = programs.hard
    soft: Union[Program, str] = programs.soft
    optimize: Union[Program, str] = programs.optimize
    weights: Union[Weights, dict] = draco_weights


Specification = Union[str, Iterable[str]]


class CheckSpecDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to check a specification via ``Draco.check_spec``."""

    spec: Specification


CheckSpecReturn = bool


class CompleteSpecDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to complete a specification via ``Draco.complete_spec``."""

    spec: Specification
    models: int = 1


CompleteSpecReturn = List[Model]


class CountPreferencesDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to count preferences via ``Draco.count_preferences``."""

    spec: Specification


CountPreferencesReturn = Optional[DefaultDict[str, int]]


class GetViolationsDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to get violations via ``Draco.get_violations``."""

    spec: Specification


GetViolationsReturn = Optional[List[str]]


class RunClingoDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to run clingo via ``draco.run.run_clingo``."""

    program: Union[str, Iterable[str]]
    models: int = 0
    topK: bool = False
    arguments: List[str] = []


RunClingoReturn = List[Model]