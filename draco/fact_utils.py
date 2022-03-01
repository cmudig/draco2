import itertools
from collections import defaultdict
from enum import Enum, unique
from typing import Generator, Iterable, Iterator, List, Mapping, Optional, Tuple, Union

from clingo import Symbol
from clingo.symbol import SymbolType


@unique
class FactKind(Enum):
    """The kind of ASP fact.

    Attributes:
        :ENTITY: a nested entity ("is a" relationship)
        :ATTRIBUTE: an attribute (value)
    """

    ENTITY = "entity"
    ATTRIBUTE = "attribute"


# the root object that is not the entity of any other object
ROOT = "root"


def stringify(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return stringify(value[0])
        return "({})".format(",".join(map(stringify, value)))

    value = str(value)
    return value[:1].lower() + value[1:]


def make_fact(kind: FactKind, values: Iterable = []) -> str:
    """Create an ASP fact from a list of values. The function generates either
    attribute or entity facts.
    """
    parts = stringify(values)
    return f"{kind.value}{parts}."


def dict_to_facts(
    data: Union[Mapping, List, str],
    path: Tuple = (),
    parent: Union[str, int] = ROOT,
    id_generator: Optional[Iterator[int]] = None,
) -> List[str]:
    """A generic encoder for dictionaries as answer set programming facts.

    The encoder can convert dictionaries as well as lists (generating
    identifiers as numbers).

    The inverse of this function is :code:`answer_set_to_dict`.
    """
    return list(_dict_to_facts(data, path, parent, id_generator))


def _dict_to_facts(
    data: Union[Mapping, List, str],
    path: Tuple = (),
    parent: Union[str, int] = ROOT,
    id_generator: Optional[Iterator[int]] = None,
) -> Generator[str, None, None]:
    if id_generator is None:
        id_generator = itertools.count()

    if isinstance(data, Mapping):
        for prop, obj in data.items():
            yield from _dict_to_facts(obj, path + (prop,), parent, id_generator)
    else:
        if isinstance(data, list):
            for obj in data:
                entity_id: Union[str, int] = 0
                if "__id__" in obj:
                    entity_id = obj["__id__"]
                else:
                    try:
                        entity_id = next(id_generator)
                    except StopIteration:  # pragma: no cover
                        # should never happen but guards against
                        # https://www.python.org/dev/peps/pep-0479/
                        pass

                path_tail = (path[-1],)
                yield make_fact(FactKind.ENTITY, (path_tail, parent, entity_id))
                yield from _dict_to_facts(obj, path_tail, entity_id, id_generator)
        elif not path[-1].startswith("__"):  # ignore keys that start with "__"
            if isinstance(data, bool):
                # special cases for boolean values
                fact = make_fact(
                    FactKind.ATTRIBUTE,
                    (path, parent),
                )
                if data:
                    yield fact
                else:
                    yield f":- {fact}"
            else:
                yield make_fact(
                    FactKind.ATTRIBUTE,
                    (path, parent, data),
                )


def get_value(symbol: Symbol):
    """Get the value of a Clingo symbol."""
    if symbol.type == SymbolType.Number:
        return symbol.number
    elif symbol.type == SymbolType.Function:
        if len(symbol.arguments):
            return tuple(map(get_value, symbol.arguments))
        return symbol.name
    else:  # pragma: no cover
        raise ValueError("Unsupported type")


def collect_children(name: str, collector: dict):
    """Helper function to collect the children for a name into a dictionary."""
    out: dict = {}

    for prop, value in collector[name].items():
        if isinstance(prop, tuple):
            prop = prop[-1]
        if isinstance(value, list):
            out[prop] = [collect_children(child, collector) for child in value]
        else:
            out[prop] = value

    return out


def answer_set_to_dict(answer_set: Iterable[Symbol], root=ROOT) -> Mapping:
    """A generic decoder that converts an answer set into a nested data structure.
    The inverse of this function is :code:`dict_to_facts`.
    """

    collector: dict = defaultdict(dict)

    for symbol in answer_set:
        if symbol.match("attribute", 3):
            prop, obj, val = map(get_value, symbol.arguments)
            collector[obj][prop] = val
        elif symbol.match("entity", 3):
            prop, obj, child = map(get_value, symbol.arguments)
            collector[obj][prop] = collector[obj].get(prop, []) + [child]

    return collect_children(root, collector)
