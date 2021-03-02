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


def deep_nest(root: Dict[Union[str, int], Any], current_dict: Dict):
    """Indexes into the memo dictionary and creates the nested data structure"""
    for key in current_dict:
        # replacing ids (ints) in lists with the corresponding values in root
        if isinstance(current_dict[key], list):
            current_list = current_dict[key]
            for i, element in enumerate(current_list):
                if isinstance(element, int) and element in root:
                    index = element
                    current_list[i] = root[index]
                deep_nest(root, current_list[i])
        # go deeper into nested dicts to look for ids (ints) to replace
        elif isinstance(current_dict[key], Mapping):
            deep_nest(root, current_dict[key])
    return


def remove_memo(root: Dict[Union[str, int], Any]):
    """
    Removes the integer ID mappings in the dictionary
    """
    to_delete = [key for key in root if isinstance(key, int)]
    for key in to_delete:
        del root[key]

    return


def parse_values(values: List) -> List:
    """
    If the value is a number, the function converts the string to a nuumber
    and return the string otherwise
    """
    result = []
    for value in values:
        if value.type == SymbolType.Function:
            name, args = value.name, value.arguments
            # strings are parsed as SymbolType functions with no arguments
            if args == []:
                result.append(name)
            # functions are parsed as SymbolType functions with >=1 arguments
            else:
                result.append(tuple(parse_values(list(args))))
        else:
            result.append(value.number)
    return result


def handle_path(
    address: List[Union[str, int]], value: Any, nested_dict: Dict, kind: FactKind
) -> Dict[Union[str, int], Any]:

    """Unpacks address tuples into nested dictionaries and adds them to the
    appropriate root/ parent_index dictionary
    """
    # nested_dict is destination dictionary
    if len(address) == 1:
        last = address[0]
        if kind == FactKind.ATTRIBUTE.value:
            nested_dict[last] = value
        else:
            if last in nested_dict:
                nested_dict[last].append(value)
            else:
                nested_dict[last] = [value]
        return nested_dict
    # there are some nested dicts to get through
    else:
        elem = address[0]
        # if the successive dict in the address has been created already
        if elem in nested_dict:
            nested_dict[elem] = handle_path(address[1:], value, nested_dict[elem], kind)
        else:
            nested_dict[elem] = handle_path(address[1:], value, dict(), kind)
        return nested_dict


def facts_to_dict(facts: List) -> Mapping:
    """A generic decoder that converts an answer set into a nested data structure"""

    root: Dict[Union[str, int], Any] = dict()
    # Creating the memo dictionary that maps ids to nested properties
    for fact in facts:
        kind, values = fact.name, fact.arguments
        parsed_values = parse_values(values)
        key, parent_index, val = parsed_values
        if kind == FactKind.PROPERTY.value:
            if parent_index == ROOT:
                # if the destination has an address
                if type(key) == tuple:
                    root = handle_path(list(key), val, root, kind)
                # if the current dictionary is the destination
                else:
                    if key in root:
                        root[key].append(val)
                    else:
                        root[key] = [val]
            else:
                # the process is identical except the parent is not root
                if type(key) == tuple:
                    root[parent_index] = handle_path(
                        list(key), val, root[parent_index], kind
                    )
                else:
                    if key in root[parent_index]:
                        root[parent_index][key].append(val)
                    else:
                        root[parent_index][key] = [val]
            # adding property's id as a key to root
            if val not in root:
                root[val] = dict()
        else:
            if parent_index == ROOT:
                # if the destination has an address
                if type(key) == tuple:
                    root = handle_path(list(key), val, root, kind)
                # if the current dictionary is the destination
                else:
                    root[key] = val
            else:
                if parent_index not in root:
                    # if facts are not in order and parent index doesn't exist
                    root[parent_index] = dict()
                # the process is identical except the parent is not root
                if type(key) == tuple:
                    root[parent_index] = handle_path(
                        list(key), val, root[parent_index], kind
                    )
                else:
                    root[parent_index][key] = val

    deep_nest(root, root)
    # Removing integer ID -> property mappings from the dictionary
    remove_memo(root)
    return root
