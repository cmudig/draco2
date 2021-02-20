from collections import abc
from enum import Enum, unique
from typing import Any, Dict, Generator, List, Mapping, Tuple, Union

from clingo import SymbolType


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
    start_id=0,
) -> Generator[str, None, None]:
    """A generic encoder for dictionaries as answer set programming facts.

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


def parse_values(values: List) -> Any:
    """
    If the value is a number, the function converts the string to a nuumber
    and return the string otherwise
    """
    for i in range(len(values)):
        if values[i].type == SymbolType.Function:
            name, args = values[i].name, values[i].arguments
            if args == []:
                values[i] = name
            else:
                values[i] = tuple(parse_values(list(args)))
        elif values[i].type == SymbolType.Number:
            values[i] = values[i].number
        else:
            values[i] = values[i].string
    return values


def handle_path(address, value, nested_dict):
    assert len(address) != 0
    if len(address) == 1:
        last = address[0]
        nested_dict[last] = value
        return nested_dict

    else:
        elem = address[0]
        if elem in nested_dict:
            nested_dict[elem] = handle_path(address[1:], value, nested_dict[elem])
        else:
            nested_dict[elem] = handle_path(address[1:], value, dict())
        return nested_dict


def facts_to_dict(facts: List) -> Mapping:
    """
    A generic decoder that converts an answer set into a nested data structure

    """
    Root: Dict[Union[int, str], Any] = dict()
    print(len(facts))
    # Creating the memo dictionary that maps numbers to nested properties
    if facts == []:
        return Root
    for fact in facts:
        assert fact.type == SymbolType.Function
        kind, values = fact.name, fact.arguments
        key, parent_index, val = parse_values(values)
        if kind == FactKind.PROPERTY.value:
            if parent_index == ROOT:
                if type(key) == tuple:
                    Root = handle_path(list(key), val, Root)
                else:
                    if key in Root:
                        Root[key].append(val)
                    else:
                        Root[key] = [val]
            else:
                if type(key) == tuple:
                    Root[parent_index] = handle_path(list(key), val, Root[parent_index])
                if key in Root[parent_index]:
                    Root[parent_index][key].append(val)
                else:
                    Root[parent_index][key] = [val]

            if val not in Root:
                Root[val] = dict()
        else:
            if parent_index == ROOT:
                if type(key) == tuple:
                    Root = handle_path(list(key), val, Root)
                else:
                    Root[key] = val
            else:
                if parent_index not in Root:
                    Root[parent_index] = dict()
                if type(key) == tuple:
                    Root[parent_index] = handle_path(list(key), val, Root[parent_index])
                else:
                    Root[parent_index][key] = val
        print("ROOT", Root)
    # Running through the memoized dictionary to replace the integer ID
    # with the actual property
    deep_nest(Root, Root)
    # Removing integer ID -> property mappings from the dictionary
    remove_memo(Root)
    print(Root)
    return Root
