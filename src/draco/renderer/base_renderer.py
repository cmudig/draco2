from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pandas import DataFrame

T = TypeVar("T")


class BaseRenderer(ABC, Generic[T]):
    """
    Base class for all renderers.
    Should handle the creation of a visualization
    represented as an object of type `T`.
    """

    @abstractmethod
    def render(self, spec: dict, data: DataFrame) -> T:
        """
        Render a visualization from a dictionary-based specification and data.

        :param spec: Specification of the visualization.
        :param data: Data to render.
        :return: Produced visualization object of type `T`.
        """
        raise NotImplementedError  # pragma: no cover
