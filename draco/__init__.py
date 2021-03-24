import pkg_resources

from draco import programs

from .fact_utils import answer_set_to_dict, dict_to_facts
from .run import is_satisfiable, run_clingo
from .schema import schema_from_dataframe, schema_from_file
from .spec import check_spec, get_violations
from .utils import dict_union

__version__ = pkg_resources.get_distribution("draco").version

__all__ = [
    "programs",
    "dict_to_facts",
    "answer_set_to_dict",
    "run_clingo",
    "is_satisfiable",
    "check_spec",
    "get_violations",
    "schema_from_dataframe",
    "schema_from_file",
    "dict_union",
]
