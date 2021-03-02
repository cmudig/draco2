import itertools
from collections import abc, defaultdict
from enum import Enum, unique
from typing import Generator, Iterator, List, Mapping, Tuple, Union

from clingo import Symbol
from clingo.symbol import SymbolType


@unique
class FactKind(Enum):
    """The kind of ASP fact.

    Attributes:
        :PROPERTY: a nested property ("is a" relationship)
        :ATTRIBUTE: an attribute (value)
    """

    PROPERTY = "property"
    ATTRIBUTE = "attribute"


# the root object that is not the property of any other object
ROOT = "root"


def stringify(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return stringify(value[0])
        return "({})".format(",".join(map(stringify, value)))

    value = str(value)
    return value[:1].lower() + value[1:]


def make_fact(kind: FactKind, values=List) -> str:
    """Create an ASP fact from a list of values. The function generates either
    attribute or property facts.
    """
    parts = stringify(values)
    return f"{kind.value}{parts}."


def dict_to_facts(
    data: Union[Mapping, List, str],
    path: Tuple = (),
    parent: str = ROOT,
    id_generator: Iterator[int] = None,
) -> Generator[str, None, None]:
    """A generic encoder for dictionaries as answer set programming facts.

    The encoder can convert dictionaries as well as lists (generating
    identifiers as numbers).

    The inverse of this function is `answer_set_to_dict`.
    """

    if id_generator is None:
        id_generator = itertools.count()

    if isinstance(data, abc.Mapping):
        for prop, obj in data.items():
            yield from dict_to_facts(obj, path + (prop,), parent, id_generator)
    else:
        if isinstance(data, list):
            for obj in data:
                if "__id__" in obj:
                    object_id = obj["__id__"]
                else:
                    try:
                        object_id = next(id_generator)
                    except StopIteration:
                        # should never happen but guards against
                        # # https://www.python.org/dev/peps/pep-0479/
                        pass

                yield make_fact(FactKind.PROPERTY, (path, parent, object_id))
                yield from dict_to_facts(obj, (), object_id, id_generator)
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
                yield make_fact(FactKind.ATTRIBUTE, (path, parent, data))


def get_value(symbol: Symbol):
    """Get the value of a Clingo symbol."""
    if symbol.type == SymbolType.Number:
        return symbol.number
    elif symbol.type == SymbolType.String or symbol.type == SymbolType.Function:
        return symbol.name


def collect_children(name: str, collector: dict):
    """Helper function to collect the children for a name into a dictionary."""
    out = {}

    for prop, value in collector[name].items():
        if isinstance(value, list):
            children = [collect_children(child, collector) for child in value]
            out[prop] = children
        else:
            out[prop] = value

    return out


def answer_set_to_dict(answer_set: List[Symbol]) -> Mapping:
    """A generic decoder that converts an answer set into a nested data structure.
    The inverse of this function is `dict_to_facts`.
    """

    collector: dict = defaultdict(dict)

    for symbol in answer_set:
        if symbol.match("attribute", 3):
            prop = symbol.arguments[0].name
            obj = get_value(symbol.arguments[1])
            val = get_value(symbol.arguments[2])
            collector[obj][prop] = val
        elif symbol.match("property", 3):
            prop = symbol.arguments[0].name
            obj = get_value(symbol.arguments[1])
            child = get_value(symbol.arguments[2])
            children = collector[obj].get(prop, [])
            children.append(child)
            collector[obj][prop] = children

    return collect_children("root", collector)
