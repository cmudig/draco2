from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pandas import DataFrame

from ..types import SpecificationDict

T = TypeVar("T")


class BaseRenderer(ABC, Generic[T]):
    @abstractmethod
    def build(self, spec: SpecificationDict, data: DataFrame) -> T:
        raise NotImplementedError

    @abstractmethod
    def display(self, product: T) -> None:
        raise NotImplementedError

    def render(self, spec: SpecificationDict, data: DataFrame) -> None:
        product = self.build(spec, data)
        self.display(product)
