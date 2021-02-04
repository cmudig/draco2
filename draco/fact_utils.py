from collections import abc
from enum import Enum, unique
from typing import Generator, List, Mapping


@unique
class FactKind(Enum):
    # a nested property ("is a" relationship)
    PROPERTY = "property"
    # an attribute (value)
    ATTRIBUTE = "attribute"


# the root object that is not the property of any other object
ROOT = "root"


def make_fact(kind: FactKind, values=List, short=False) -> str:
    """
    Create an ASP fact from a list of values. The function can generate both a
    long form (`fact(x,y,z)`) and a short form (`x(y,z)`). The short form uses
    the first element as the name of the fact. The short form ignores the fact kind.
    """
    if short:
        rest = ",".join(map(str, values[1:]))
        return f"{values[0]}({rest})."
    else:
        parts = ",".join(map(str, values))
        return f"{kind.value}({parts})."


def dict_to_facts(
    data: Mapping, parent: str = ROOT, short=False, start_id=0
) -> Generator[str, None, None]:
    """
    A generic encoder for dictionaries as answer set programming facts.

    The encoder can convert dictionaries in dictionaries (using the keys as
    names) as well as lists (generating identifiers as numbers).
    """
    for key, value in data.items():
        if isinstance(value, abc.Mapping):
            for prop, obj in value.items():
                yield make_fact(FactKind.PROPERTY, (key, parent, prop), short)
                yield from dict_to_facts(obj, prop, short)
        elif isinstance(value, list):
            for obj in value:
                object_id = start_id
                start_id += 1

                yield make_fact(FactKind.PROPERTY, (key, parent, object_id), short)
                yield from dict_to_facts(obj, object_id, short, start_id)
        else:
            yield make_fact(
                FactKind.ATTRIBUTE,
                (key, parent, value),
                short,
            )


def facts_to_dict(facts: List) -> Mapping:
    """
    A generic decoder that converts an answer set into a nested data structure
    """
    pass  # TODO: https://github.com/cmudig/draco2/issues/24
