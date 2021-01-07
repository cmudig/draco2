from collections import abc
from typing import Generator, List, Mapping


def make_fact(values=List, short=False) -> str:
    """
    Create an ASP fact from a list. The function can generate both a
    long form (`fact(x,y,z)`) and a short form (`x(y,z)`). The short form uses
    the first element as the name of the fact.
    """
    if short:
        rest = ",".join(map(str, values[1:]))
        return f"{values[0]}({rest})."
    else:
        parts = ",".join(map(str, values))
        return f"fact({parts})."


def dict_to_facts(
    data: Mapping, fact_key: str = None, short=False
) -> Generator[str, None, None]:
    """
    A generic encoder for dictionaries as answer set programming facts.
    """
    for key, value in data.items():
        if isinstance(value, abc.Mapping):
            if fact_key is not None:
                yield make_fact((fact_key, key), short)
            yield from dict_to_facts(value, key)
        else:
            yield make_fact((key, fact_key, value) if fact_key else (key, value), short)


def facts_to_dict(facts: List) -> Mapping:
    """
    A generic decoder that converts an answer set into a nested data structure
    """
    pass  # TODO: https://github.com/cmudig/draco2/issues/24
