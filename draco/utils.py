from itertools import chain


def dict_union(*args: dict):
    return dict(chain.from_iterable(d.items() for d in args))


def dict_value_by_path(d: dict, path: tuple):
    for key in path:
        d = d[key]
    return d
