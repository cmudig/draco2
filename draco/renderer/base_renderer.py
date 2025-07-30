from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeAlias, TypeVar, Union

from narwhals.typing import IntoDataFrame

DataType: TypeAlias = Union[dict[Any, Any], IntoDataFrame]
LabelMapping: TypeAlias = Union[dict[str, str], Callable[[str], str]]

T = TypeVar("T")


class BaseRenderer(ABC, Generic[T]):
    """
    Base class for all renderers.
    Should handle the creation of a visualization
    represented as an object of type `T`.
    """

    @abstractmethod
    def render(
        self, spec: dict, data: DataType, label_mapping: LabelMapping | None = None
    ) -> T:
        """
        Render a visualization from a dictionary-based specification and data.

        :param spec: Specification of the visualization.
        :param data: Data to render.
        :param label_mapping: Mapping of field names to human-readable labels.
            If a callable is provided, it will be called with the field name
            and should return a human-readable label.
        :return: Produced visualization object of type `T`.
        """
        raise NotImplementedError  # pragma: no cover
