import pkg_resources

from draco import programs

from .fact_utils import dict_to_facts
from .run import is_satisfiable, run_clingo
from .schema import schema_from_dataframe, schema_from_file

__version__ = pkg_resources.get_distribution("draco").version

__all__ = [
    "programs",
    "dict_to_facts",
    "run_clingo",
    "is_satisfiable",
    "schema_from_dataframe",
    "schema_from_file",
]
