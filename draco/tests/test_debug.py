import itertools
from typing import Iterable

import altair as alt
import pandas as pd
import pytest

from draco.debug import ChartConfig, DracoDebug, DracoDebugPlotter

specs: dict[str, Iterable[str] | str] = {
    "tick_plot": """
    attribute(number_rows,root,100).
    entity(field,root,temperature).
    attribute((field,name),temperature,temperature).
    attribute((field,type),temperature,number).
    entity(view,root,0).
    entity(mark,0,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(scale,0,3).
    attribute((scale,channel),3,x).
    attribute((scale,type),3,linear).
""",
    "tick_plot_log": """
    attribute(number_rows,root,100).
    entity(field,root,temperature).
    attribute((field,name),temperature,temperature).
    attribute((field,type),temperature,number).
    entity(view,root,0).
    entity(mark,0,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(scale,0,3).
    attribute((scale,channel),3,x).
    attribute((scale,type),3,log).
""",
}


def test_init():
    # init should work without raising exceptions
    instance = DracoDebug(specs=specs)
    assert type(instance) is DracoDebug


def test_chart_preferences():
    instance = DracoDebug(specs=specs)
    df = instance.chart_preferences
    rows, cols = df.shape
    assert cols == 4
    assert rows == len(instance.specs) * len(instance.feature_names)


def __create_test_data(num_data_rows: int = 10) -> pd.DataFrame:
    return pd.DataFrame(
        data=[("x", "y", i, i % 4) for i in range(1, num_data_rows + 1)],
        columns=["chart_name", "pref_name", "count", "weight"],
    )


@pytest.mark.parametrize(
    "data",
    [__create_test_data(0), __create_test_data(5)],
)
def test_plotter_init(data):
    instance = DracoDebugPlotter(chart_preferences=data)
    assert type(instance) is DracoDebugPlotter


def __create_test_debug_plotter(num_data_rows: int = 10) -> DracoDebugPlotter:
    data = __create_test_data(num_data_rows)
    return DracoDebugPlotter(chart_preferences=data)


# Running `test_plotter_create_chart` param combinations
# using data frames with this many rows against each config
__num_data_row_test_cases = [0, 100, 1000, 10_000]

# Running `test_plotter_create_chart` with these configs
__chart_config_test_cases = [
    None,
    *DracoDebugPlotter.__DEFAULT_CONFIGS__,
    ChartConfig(title="Test Title", sort_x=None, sort_y=None),
]
# Produces the `"instance,config"` tuples for `@pytest.mark.parametrize`
__create_chart_test_cases = list(
    itertools.product(
        map(__create_test_debug_plotter, __num_data_row_test_cases),
        __chart_config_test_cases,
    )
)


@pytest.mark.parametrize(
    "instance,config",
    __create_chart_test_cases,
)
def test_plotter_create_chart(instance: DracoDebugPlotter, config: ChartConfig):
    chart = instance.create_chart(cfg=config)

    # Expect a vertically concatenated chart made up of two sub-plots
    assert type(chart) is alt.VConcatChart and len(chart.vconcat) == 2


@pytest.mark.parametrize(
    "instance,config",
    __create_chart_test_cases,
)
def test_plotter_create_chart_used_data(
    instance: DracoDebugPlotter, config: ChartConfig
):
    chart = instance.create_chart(cfg=config)

    # The passed data should be used for visualization
    assert pd.DataFrame.eq(chart.data, instance.chart_preferences).all().all()


@pytest.mark.parametrize(
    "instance,config",
    __create_chart_test_cases,
)
def test_plotter_create_chart_title(instance: DracoDebugPlotter, config: ChartConfig):
    chart = instance.create_chart(cfg=config)

    # Expect that the configured title is used
    if config is not None:
        assert chart.title == config.title


def __mark_as_str(mark: str | alt.MarkDef) -> str:
    if type(mark) is str:
        return mark
    else:
        mark_def: alt.MarkDef = mark
        return mark_def.type


@pytest.mark.parametrize(
    "instance,config",
    __create_chart_test_cases,
)
def test_plotter_create_chart_size(instance: DracoDebugPlotter, config: ChartConfig):
    chart = instance.create_chart(cfg=config)
    weight_bar_chart, pref_rect_chart = chart.vconcat
    # vertically concatenated chart -> Taking max for width and sum for height
    subplot_size_sum_width = max([weight_bar_chart.width, pref_rect_chart.width])
    subplot_size_sum_height = sum([weight_bar_chart.height, pref_rect_chart.height])
    assert (subplot_size_sum_width, subplot_size_sum_height) == instance.plot_size


@pytest.mark.parametrize(
    "instance,config",
    __create_chart_test_cases,
)
def test_plotter_create_chart_subplot_marks(
    instance: DracoDebugPlotter, config: ChartConfig
):
    chart = instance.create_chart(cfg=config)
    weight_bar_chart, pref_rect_chart = chart.vconcat

    # Expect the weight chart to use `bar` as its mark
    assert __mark_as_str(weight_bar_chart.mark) == "bar"
    # Expect the pref grid chart to use `rect` as its mark
    assert __mark_as_str(pref_rect_chart.mark) == "rect"


@pytest.mark.parametrize(
    "instance,config",
    __create_chart_test_cases,
)
def test_plotter_create_chart_subplot_sorting(
    instance: DracoDebugPlotter, config: ChartConfig
):
    chart = instance.create_chart(cfg=config)
    weight_bar_chart, pref_rect_chart = chart.vconcat

    # Expect that custom-configured sorting is used
    if config is not None:
        if config.sort_x is not None:
            assert weight_bar_chart.encoding.x.sort == config.sort_x
            assert pref_rect_chart.encoding.x.sort == config.sort_x
        if config.sort_y is not None:
            assert pref_rect_chart.encoding.y.sort == config.sort_y
