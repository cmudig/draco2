from collections import abc
from enum import Enum, unique
from typing import Any, Dict, Generator, List, Mapping, Union


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
                if "__id__" in obj:
                    object_id = obj["__id__"]
                else:
                    object_id = start_id
                    start_id += 1

                yield make_fact(FactKind.PROPERTY, (key, parent, object_id), short)
                yield from dict_to_facts(obj, object_id, short, start_id)
        elif not key.startswith("__"):  # ignore keys that start with "__"
            yield make_fact(
                FactKind.ATTRIBUTE,
                (key, parent, value),
                short,
            )


def extract_elems(fact: str):
    """
    Splits every fact into a tuple of:
    (property or attribute, list of comma separated values)
    """
    kind = fact[: fact.index("(")]
    str_values = fact[fact.index("(") + 1 : fact.index(")")]
    list_values = str_values.split(",")
    if kind == FactKind.PROPERTY.value:
        return (FactKind.PROPERTY, list_values)
    else:
        return (FactKind.ATTRIBUTE, list_values)


def deep_nest(Root: Mapping, current_dict: Mapping):
    """
    Indexes into the memo dictionary and creates the nested data structure
    """
    for key in current_dict:
        if isinstance(current_dict[key], list):
            current_list = current_dict[key]
            for i in range(len(current_list)):
                assert current_list[i] in Root
                index = current_list[i]
                current_list[i] = Root[index]
                deep_nest(Root, current_list[i])


def remove_memo(Root: Dict[Union[str, int], Any]):
    """
    Removes the integer ID mappings in the dictionary
    """
    to_delete = []
    for key in Root:
        if isinstance(key, int):
            to_delete.append(key)

    for key in to_delete:
        del Root[key]


def parse_value(val: str):
    """
    If the value is a number, the function converts the string to a nuumber
    and return the string otherwise
    """
    try:
        Numeric = float(val)
        return Numeric
    except ValueError:
        return val


def facts_to_dict(facts: List) -> Mapping:
    """
    A generic decoder that converts an answer set into a nested data structure

    """
    Root: Dict[Union[int, str], Any] = dict()
    # Creating the memo dictionary that maps numbers to nested properties
    if facts == []:
        return Root
    for fact in facts:
        kind, values = extract_elems(fact)
        (key, parent_index, val) = values
        if kind.value == FactKind.PROPERTY.value:
            if parent_index == "root":
                if key in Root:
                    Root[key].append(int(val))
                else:
                    Root[key] = [int(val)]
                Root[int(val)] = dict()
            else:
                if key in Root[int(parent_index)]:
                    Root[int(parent_index)][key].append(int(val))
                else:
                    Root[int(parent_index)][key] = [int(val)]
                Root[int(val)] = dict()
        else:
            if parent_index == "root":
                Root[key] = parse_value(val)
            else:
                Root[int(parent_index)][key] = parse_value(val)
    # Running through the memoized dictionary to replace the integer ID
    # with the actual property
    deep_nest(Root, Root)
    # Removing integer ID -> property mappings from the dictionary
    remove_memo(Root)
    return Root
