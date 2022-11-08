from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from typing import Generic, Optional, TypeVar

from pandas import DataFrame

from draco.utils import dict_value_by_path

T = TypeVar("T")
SpecProperty = str | int | float | bool | None | dict | list


@dataclass(frozen=True)
class _VisitedItemRaw(Generic[T]):
    value: SpecProperty
    path: tuple[int | str, ...]
    acc: T = field(repr=False)


@dataclass(frozen=True)
class VisitedItem(Generic[T]):
    item: _VisitedItemRaw[T]
    spec: dict = field(repr=False)

    @property
    def value(self) -> SpecProperty:
        return self.item.value

    @property
    def path(self) -> tuple[int | str, ...]:
        return self.item.path

    @property
    def acc(self) -> T:
        return self.item.acc

    @property
    def type(self) -> str:
        is_list_element = isinstance(self.path[-1], int)
        if is_list_element:
            return self.path[-2]
        return self.path[-1]

    @cached_property
    def parent(self) -> Optional["VisitedItem"]:
        raw_parent = self.__parent()
        if raw_parent is not None:
            return VisitedItem(item=raw_parent, spec=self.spec)
        return None

    def __parent(self) -> _VisitedItemRaw | None:
        has_parent = len(self.path) > 1
        if has_parent:
            parent_path = self.path[:-1]
            parent_value = dict_value_by_path(self.spec, parent_path)
            return _VisitedItemRaw(parent_value, parent_path, self.acc)
        return None


class BaseRenderer(ABC, Generic[T]):
    """
    Base class for all renderers.
    """

    def __init__(self, spec: dict, df: DataFrame):
        """
        Creates a new renderer for the specified specification and data frame.

        :param spec: dictionary-based specification
        :param df: data frame to be rendered
        """
        self.spec = spec
        self.df = df

    def build(self) -> T:
        """
        Builds a concrete rendering product of type `T` from `self.spec` and `self.df`.
        The rendering object's actual type depends on the concrete renderer.
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
                    VisitedItem(
                        item=_VisitedItemRaw(value=dct, path=path, acc=acc),
                        spec=self.spec,
                    )
                )

            for key, value in dct.items():
                if isinstance(value, dict):
                    acc = traverse(value, path + (key,), acc)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        acc = traverse(item, path + (key, i), acc)
                else:
                    acc = self._visitor(
                        VisitedItem(
                            item=_VisitedItemRaw(
                                value=value, path=path + (key,), acc=acc
                            ),
                            spec=self.spec,
                        )
                    )
            return acc

        product = traverse(dct=self.spec, path=(), acc=self._initial)
        post_processed = self.post_build_hook(product)
        return post_processed

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

    def post_build_hook(self, product: T) -> T:
        """
        Called after the traversal of the specification is completed.
        Acts as a hook for post-processing the rendering product.
        :return: the updated rendering product
        """
        return product
