from collections import defaultdict
from enum import Enum
from functools import cached_property
from typing import Iterable, NamedTuple

import altair as alt
import pandas as pd

from .asp_utils import Block, parse_blocks
from .draco import Draco

PrefTuple = tuple[str, str, int]
PrefTupleWithDescription = tuple[str, str, str, int]
PrefTupleWithDescriptionWeighted = tuple[str, str, str, int, int]


class DracoDebug:
    """
    Class to aid the debugging of visualization specifications against
    the knowledge base of a Draco instance. Methods exposed by this class
    give insight into the constraints and weights defined in the Draco instance and
    how they are violated by the supplied visualization specifications.
    """

    __DEFAULT_DRACO__ = Draco()

    def __init__(
        self,
        specs: dict[str, Iterable[str] | str],
        draco: Draco = __DEFAULT_DRACO__,
    ):
        """
        Initializes a new debugger instance.

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
    def feature_descriptions(self) -> dict[str, str]:
        """
        :return: a dict mapping feature names to their descriptions
        """
        # Dict returning "N/A" by default as description for a feature
        dct: dict[str, str] = defaultdict(lambda: "N/A")
        soft_constraint_program_blocks = parse_blocks(self.draco.soft)
        for feature, block in soft_constraint_program_blocks.items():
            if isinstance(feature, str) and isinstance(block, Block):
                dct[feature] = block.description
        return dct

    @cached_property
    def chart_preferences(self) -> pd.DataFrame:
        """
        Returns a ``DataFrame`` with four columns:

        * ``chart_name``: Specification name, a key of ``self.specs``
        * ``pref_name``: Preference (feature) name,
                         element of ``self.feature_names``
        * ``pref_description``: Preference (feature) description.
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
        pref_tuples_with_descriptions = self.__pref_tuples_extended_with_descriptions(
            pref_tuples, self.feature_descriptions
        )
        pref_tuples_with_weights = self.__pref_tuples_extended_with_weights(
            pref_tuples_with_descriptions, self.draco.weights
        )
        return pd.DataFrame(
            data=pref_tuples_with_weights,
            columns=["chart_name", "pref_name", "pref_description", "count", "weight"],
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
    def __unnest_pref_count_dict(dct: dict[str, dict[str, int]]) -> list[PrefTuple]:
        """Flattens the dict of dicts into a list of tuples"""
        return [
            (chart_name, pref_name, count)
            for chart_name, prefs in dct.items()
            for pref_name, count in prefs.items()
        ]

    @staticmethod
    def __pref_tuple_extended_with_descriptions(
        tpl: PrefTuple, descriptions: dict[str, str]
    ) -> PrefTupleWithDescription:
        """
        Extends a ``(chart_name, pref_name, count)``
        tuple to include ``weight`` as its last element.
        """
        chart_name, pref_name, count = tpl
        pref_description = descriptions[pref_name]
        return chart_name, pref_name, pref_description, count

    @staticmethod
    def __pref_tuples_extended_with_descriptions(
        tuples: list[PrefTuple], descriptions: dict[str, str]
    ) -> list[PrefTupleWithDescription]:
        cls = DracoDebug
        return [
            cls.__pref_tuple_extended_with_descriptions(tpl, descriptions)
            for tpl in tuples
        ]

    @staticmethod
    def __pref_tuple_extended_with_weight(
        tpl: PrefTupleWithDescription, weights: dict[str, int]
    ) -> PrefTupleWithDescriptionWeighted:
        """
        Extends a ``(chart_name, pref_name, count)``
        tuple to include ``weight`` as its last element.
        """
        chart_name, pref_name, pref_description, count = tpl
        weight = weights[f"{pref_name}_weight"]
        return chart_name, pref_name, pref_description, count, weight

    @staticmethod
    def __pref_tuples_extended_with_weights(
        tuples: list[PrefTupleWithDescription], weights: dict[str, int]
    ) -> list[PrefTupleWithDescriptionWeighted]:
        cls = DracoDebug
        return [cls.__pref_tuple_extended_with_weight(tpl, weights) for tpl in tuples]


class ChartConfig(NamedTuple):
    title: str
    sort_x: alt.Sort | str | None
    sort_y: alt.Sort | str | None


class DracoDebugChartConfig(Enum):
    SORT_ALPHABETICALLY = ChartConfig(
        title="Sort alphabetically", sort_x="ascending", sort_y="ascending"
    )
    SORT_BY_COUNT_SUM = ChartConfig(
        title="Sort by count sum",
        sort_x=alt.EncodingSortField(field="count", op="sum", order="descending"),
        sort_y=alt.EncodingSortField(field="count", op="sum", order="descending"),
    )

    @staticmethod
    def by_title(title: str) -> "DracoDebugChartConfig":
        for config in DracoDebugChartConfig:
            if config.value.title == title:
                return config
        raise ValueError(f"Unknown chart config title: {title}")


class DracoDebugPlotter:
    """
    Class to aid the plotting of Draco debug data
    produced by ``DracoDebug.chart_preferences``.
    """

    # width, height
    __DEFAULT_CELL_SIZE__: tuple[float, float] = (30, 30)
    __DEFAULT_PLOT_SIZE__: tuple[float, float] = (1200, 400)

    def __init__(
        self,
        chart_preferences: pd.DataFrame,
    ):
        """
        Initializes a new plotter instance, to be used
        to create charts visualizing the Draco debug data.

        :param chart_preferences: the ``DataFrame``
                                  returned by ``DracoDebug.chart_preferences``
        """
        self.chart_preferences = chart_preferences

    @staticmethod
    def _compute_ideal_plot_size(
        chart_preferences: pd.DataFrame,
    ) -> tuple[float, float]:
        cell_width, cell_height = DracoDebugPlotter.__DEFAULT_CELL_SIZE__
        num_prefs = len(set(chart_preferences["pref_name"]))
        num_charts = len(set(chart_preferences["chart_name"]))

        width = num_prefs * cell_width
        # The heatmap has 3/4 the height of the full chart
        heatmap_height = num_charts * cell_height
        height = (4 / 3) * heatmap_height
        width_max, height_max = DracoDebugPlotter.__DEFAULT_PLOT_SIZE__
        return (width, height) if width < width_max else (width_max, height_max)

    def create_chart(
        self,
        *,
        cfg: DracoDebugChartConfig | ChartConfig | None = None,
        violated_prefs_only: bool = False,
        plot_size: tuple[float, float] | None = None,
    ) -> alt.VConcatChart:
        """
        Creates a vertically concatenated chart made up of
        an aligned bar chart visualizing feature weights
        and a heatmap visualizing the number of times each spec violates each feature.

        :param cfg: the configuration based on which the chart title and sorting is set.
                    A default configuration will be used of this is not specified,
                    featuring an alphabetical sort by feature name and spec name.
        :param violated_prefs_only: whether to only include features that are violated
                                    by at least one spec. Defaults to ``False``.
        :param plot_size: the size of the plot described as a tuple of (width, height).
        :return: the above-described Altair chart
        """
        used_config: ChartConfig = DracoDebugChartConfig.SORT_ALPHABETICALLY.value
        if cfg is not None:
            used_config = cfg if isinstance(cfg, ChartConfig) else cfg.value

        chart_preferences = self.chart_preferences
        if violated_prefs_only:
            chart_preferences = chart_preferences[
                chart_preferences["count"] != 0
            ].reset_index()

        width, height = plot_size or DracoDebugPlotter._compute_ideal_plot_size(
            chart_preferences
        )

        return self.__create_chart(
            chart_preferences=chart_preferences,
            cfg=used_config,
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
                y=alt.Y(
                    field="weight", type="quantitative", aggregate="min", title="Weight"
                ),
                tooltip=["pref_name", "weight"],
            )
            .properties(width=width, height=height / 4)
        )
        pref_rect = (
            alt.Chart(chart_preferences)
            .mark_rect(stroke="lightgray", strokeWidth=0.25)
            .encode(
                x=alt.X(
                    field="pref_name",
                    type="nominal",
                    sort=cfg.sort_x,
                    title="Constraint",
                ),
                y=alt.Y(
                    field="chart_name",
                    type="nominal",
                    sort=cfg.sort_y,
                    title="Chart specification",
                ),
                # Set rect color to white if `count == 0`
                color=alt.condition(
                    alt.datum.count == 0,
                    alt.value("white"),
                    alt.Color(
                        field="count",
                        type="quantitative",
                        # Only show integer values in the legend
                        legend=alt.Legend(
                            labelExpr="datum.value == ceil(datum.value) "
                            "? datum.value "
                            ": ''"
                        ),
                    ),
                ),
                tooltip=chart_preferences.columns.tolist(),
            )
            .properties(width=width, height=3 * height / 4)
        )
        return alt.VConcatChart(
            vconcat=[weight_bar, pref_rect], spacing=0, title=cfg.title
        )
