from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from draco.utils import dict_value_by_path

T = TypeVar("T")
SpecProperty = str | int | float | bool | None | dict | list


@dataclass(frozen=True, kw_only=True)
class VisitedItem(Generic[T]):
    value: SpecProperty
    path: tuple[int | str, ...]
    acc: T = field(repr=False)
    spec: dict = field(repr=False)

    @property
    def parent(self) -> Optional["VisitedItem"]:
        has_parent = len(self.path) > 0
        if has_parent:
            parent_path = self.path[:-1]
            value = dict_value_by_path(self.spec, parent_path)
            return VisitedItem(
                value=value, path=parent_path, acc=self.acc, spec=self.spec
            )
        return None


class BaseRenderer(ABC, Generic[T]):
    """
    Base class for all renderers.
    """

    def render(self, spec: dict) -> T:
        """
        Render a dictionary-based specification
        into a concrete rendering product of type `T`.
        The rendering object's actual type depends on the concrete renderer.

        :param spec: dictionary-based specification
        :return: product of the rendering
        """

        def traverse(dct: dict, path: tuple[str | int, ...], acc: T):
            """
            Recursively visit a dictionary-based specification.

            :param dct: dictionary-based specification
            :param path: path to the current node
            :param acc: accumulated rendering product
            :return: the most recent rendering product
            """
            has_complex_children = any(
                isinstance(v, dict) or isinstance(v, list) for v in dct.values()
            )
            if not has_complex_children:
                return self._visitor(
                    VisitedItem(value=dct, path=path, acc=acc, spec=spec)
                )

            for key, value in dct.items():
                if isinstance(value, dict):
                    acc = traverse(value, path + (key,), acc)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        acc = traverse(item, path + (key, i), acc)
                else:
                    acc = self._visitor(
                        VisitedItem(value=value, path=path + (key,), acc=acc, spec=spec)
                    )
            return acc

        return traverse(dct=spec, path=(), acc=self._initial)

    @property
    @abstractmethod
    def _initial(self) -> T:
        """
        :return: The initial rendering product to start with.
        """
        raise NotImplementedError

    @abstractmethod
    def _visitor(self, item: VisitedItem[T]) -> T:
        """
        The callback to be invoked for each visited item of the specification.
        Should be implemented by concrete renderers to produce the rendering product
        step-by-step based on the contents of the supplied `payload`.

        :param item: the visited item
        :return: the updated rendering product
        """
        raise NotImplementedError


class VegaLiteRenderer(BaseRenderer[dict]):
    @property
    def _initial(self) -> dict:
        return {"x": 0}

    def _visitor(self, item: VisitedItem) -> dict:
        print(item)
        return {"x": item.acc["x"] + 1}


if __name__ == "__main__":
    from draco.fact_utils import answer_set_to_dict
    from draco.run import run_clingo

    def facts_to_dict(facts: list[str]):
        result = run_clingo(facts)
        return answer_set_to_dict(next(result).answer_set)

    facts = [
        "attribute(number_rows,root,100).",
        "entity(field,root,temperature).",
        "attribute((field,name),temperature,temperature).",
        "attribute((field,type),temperature,number).",
        "entity(field,root,condition).",
        "attribute((field,name),condition,condition).",
        "attribute((field,type),condition,string).",
        "entity(view,root,0).",
        "entity(mark,0,1).",
        "attribute((mark,type),1,tick).",
        "entity(encoding,1,2).",
        "attribute((encoding,channel),2,y).",
        "attribute((encoding,field),2,temperature).",
        "entity(view,root,3).",
        "entity(mark,3,4).",
        "attribute((mark,type),4,bar).",
        "entity(encoding,4,5).",
        "attribute((encoding,channel),5,y).",
        "attribute((encoding,field),5,temperature).",
        "attribute((encoding,aggregate),5,mean).",
        "entity(encoding,4,6).",
        "attribute((encoding,channel),6,x).",
        "attribute((encoding,field),6,condition).",
        "entity(scale,3,7).",
        "attribute((scale,channel),7,x).",
        "attribute((scale,type),7,ordinal).",
        "entity(scale,root,8).",
        "attribute((scale,channel),8,y).",
        "attribute((scale,type),8,linear).",
        "attribute((scale,zero),8,true).",
    ]
    spec = facts_to_dict(facts)
    from pprint import pprint

    pprint(spec)
    print()

    vl = VegaLiteRenderer()
    product = vl.render(dict(spec))
    print(product)
