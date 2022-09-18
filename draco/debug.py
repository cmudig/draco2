from functools import cached_property
from typing import Iterable, NamedTuple

import altair as alt
import pandas as pd

from .draco import Draco


class DracoDebug:
    __DEFAULT_DRACO__ = Draco()

    def __init__(
        self,
        specs: dict[str, Iterable[str] | str],
        draco: Draco = __DEFAULT_DRACO__,
    ):
        """
        Initializes a new debugging instance.

        :param specs: ``dict`` of specifications to analyze, keys representing
                       the spec name and values the corresponding ASP declarations.
        :param draco: The ``Draco`` instance to be debugged.
        """
        self.specs = specs
        self.draco = draco

    @cached_property
    def feature_names(self) -> set[str]:
        """
        :return: a set of the names of the features (constraints)
                 of the underlying Draco instance
        """
        return set(self.draco.soft_constraint_names)

    @cached_property
    def chart_preferences(self) -> pd.DataFrame:
        """
        Returns a ``DataFrame`` with four columns:

        * ``chart_name``: Specification name, a key of ``self.specs``
        * ``pref_name``: Preference (feature) name,
                         element of ``self.feature_names``
        * ``count``: The number of times the spec
                     identified by ``chart_name`` violates ``pref_name``.
        * ``weight``: The weight associated with ``pref_name``.

        The returned ``DataFrame`` always has
        ``len(self.specs) * len(self.feature_names)`` rows.

        :return: The above-described pandas ``DataFrame``.
        """
        # Nested preference counts
        pref_count_dict: dict[str, dict[str, int]] = {
            chart_name: self.__full_pref_count_dict(
                self.draco, spec, self.feature_names
            )
            for chart_name, spec in self.specs.items()
        }
        # Flattened preference counts
        pref_tuples = self.__unnest_pref_count_dict(pref_count_dict)
        pref_tuples_with_weights = self.__pref_tuples_extended_with_weights(
            pref_tuples, self.draco.weights
        )
        return pd.DataFrame(
            data=pref_tuples_with_weights,
            columns=["chart_name", "pref_name", "count", "weight"],
        )

    @staticmethod
    def __full_pref_count_dict(
        draco: Draco, spec: str | Iterable[str], feature_names: set[str]
    ) -> dict[str, int]:
        """
        Constructs a dict of preference counts,
        including all the soft constraint names in the keys
        """
        base: dict[str, int] = draco.count_preferences(spec) or {}
        included_feature_names = set(base.keys())
        not_included_feature_names = feature_names - included_feature_names
        return base | {feature_name: 0 for feature_name in not_included_feature_names}

    @staticmethod
    def __unnest_pref_count_dict(
        dct: dict[str, dict[str, int]]
    ) -> list[tuple[str, str, int]]:
        """Flattens the dict of dicts into a list of tuples"""
        return [
            (chart_name, pref_name, count)
            for chart_name, prefs in dct.items()
            for pref_name, count in prefs.items()
        ]

    @staticmethod
    def __pref_tuple_extended_with_weight(
        tpl: tuple[str, str, int], weights: dict[str, int]
    ) -> tuple[str, str, int, int]:
        """
        Extends a ``(chart_name, pref_name, count)``
        tuple to include ``weight`` as its last element.
        """
        chart_name, pref_name, count = tpl
        weight = weights[f"{pref_name}_weight"]
        return chart_name, pref_name, count, weight

    @staticmethod
    def __pref_tuples_extended_with_weights(
        tuples: list[tuple[str, str, int]], weights: dict[str, int]
    ) -> list[tuple[str, str, int, int]]:
        cls = DracoDebug
        return [cls.__pref_tuple_extended_with_weight(tpl, weights) for tpl in tuples]


class ChartConfig(NamedTuple):
    title: str
    sort_x: alt.Sort | str | None
    sort_y: alt.Sort | str | None


class DracoDebugPlotter:
    __DEFAULT_CONFIGS__: list[ChartConfig] = [
        ChartConfig(
            title="Sort alphabetically", sort_x="ascending", sort_y="ascending"
        ),
        ChartConfig(
            title="Sort by count sum",
            sort_x=alt.EncodingSortField(field="count", op="sum", order="descending"),
            sort_y=alt.EncodingSortField(field="count", op="sum", order="descending"),
        ),
    ]
    # width, height
    __DEFAULT_PLOT_SIZE__: tuple[float, float] = 1200, 400

    def __init__(
        self,
        chart_preferences: pd.DataFrame,
        chart_configs: list[ChartConfig] | None = None,
        plot_size: tuple[float, float] | None = None,
    ):
        cls = DracoDebugPlotter
        if chart_configs is None:
            chart_configs = cls.__DEFAULT_CONFIGS__
        if plot_size is None:
            plot_size = cls.__DEFAULT_PLOT_SIZE__

        self.chart_preferences = chart_preferences
        self.chart_configs = chart_configs
        self.plot_size = plot_size

    def create_chart(self, cfg: ChartConfig | None = None) -> alt.VConcatChart:
        """
        Creates a vertically concatenated chart made up of
        an aligned bar chart visualizing feature weights
        and a heatmap visualizing the number of times each spec violates each feature.

        :param cfg: the configuration based on which the chart title and sorting is set.
                    A default configuration will be used of this is not specified,
                    featuring an alphabetical sort by feature name and spec name.
        :return: the above-described Altair chart
        """
        if cfg is None:
            cfg = self.__DEFAULT_CONFIGS__[0]
        width, height = self.plot_size
        return self.__create_chart(
            chart_preferences=self.chart_preferences,
            cfg=cfg,
            width=width,
            height=height,
        )

    @staticmethod
    def __create_chart(
        chart_preferences: pd.DataFrame, cfg: ChartConfig, width: float, height: float
    ) -> alt.VConcatChart:
        weight_bar = (
            alt.Chart(chart_preferences)
            .mark_bar()
            .encode(
                x=alt.X(field="pref_name", type="nominal", sort=cfg.sort_x, axis=None),
                y=alt.Y(field="weight", type="quantitative"),
                tooltip=["pref_name", "weight"],
            )
            .properties(width=width, height=height / 4)
        )
        pref_rect = (
            alt.Chart(chart_preferences)
            .mark_rect(stroke="lightgray", strokeWidth=0.25)
            .encode(
                x=alt.X(field="pref_name", type="nominal", sort=cfg.sort_x),
                y=alt.Y(field="chart_name", type="nominal", sort=cfg.sort_y),
                # Set rect color to white if `count == 0`
                color=alt.condition(
                    alt.datum.count == 0,
                    alt.value("white"),
                    alt.Color(field="count", type="quantitative"),
                ),
                tooltip=chart_preferences.columns.tolist(),
            )
            .properties(width=width, height=3 * height / 4)
        )
        return alt.VConcatChart(
            vconcat=[weight_bar, pref_rect], spacing=0, title=cfg.title
        )
