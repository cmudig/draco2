from collections import abc
from enum import Enum, unique
from typing import Generator, List, Mapping, Tuple, Union


@unique
class FactKind(Enum):
    # a nested property ("is a" relationship)
    PROPERTY = "property"
    # an attribute (value)
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
    """
    Create an ASP fact from a list of values. The function generates either
    attribute or property facts.
    """
    parts = stringify(values)
    return f"{kind.value}{parts}."


def dict_to_facts(
    data: Union[Mapping, List, str],
    path: Tuple[str] = (),
    parent: str = ROOT,
    start_id=0,
) -> Generator[str, None, None]:
    """
    A generic encoder for dictionaries as answer set programming facts.

    The encoder can convert dictionaries as well as lists (generating
    identifiers as numbers).
    """
    if isinstance(data, abc.Mapping):
        for prop, obj in data.items():
            yield from dict_to_facts(obj, path + (prop,), parent, start_id)
    else:
        if isinstance(data, list):
            for obj in data:
                if "__id__" in obj:
                    object_id = obj["__id__"]
                else:
                    object_id = start_id
                    start_id += 1

                yield make_fact(FactKind.PROPERTY, (path, parent, object_id))
                yield from dict_to_facts(obj, (), object_id, start_id)
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


def facts_to_dict(facts: List) -> Mapping:
    """
    A generic decoder that converts an answer set into a nested data structure
    """
    pass  # TODO: https://github.com/cmudig/draco2/issues/24
    return {}
