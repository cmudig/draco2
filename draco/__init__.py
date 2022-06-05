import pkg_resources

from draco import programs

from .draco import Draco
from .fact_utils import answer_set_to_dict, dict_to_facts
from .run import is_satisfiable, run_clingo
from .schema import schema_from_dataframe, schema_from_file
from .utils import dict_union
from .weights import weights

__version__ = pkg_resources.get_distribution("draco").version

__all__ = [
    "programs",
    "dict_to_facts",
    "answer_set_to_dict",
    "run_clingo",
    "is_satisfiable",
    "Draco",
    "schema_from_dataframe",
    "schema_from_file",
    "dict_union",
    "weights",
]
