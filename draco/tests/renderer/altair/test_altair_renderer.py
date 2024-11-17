import random
from typing import Literal

import pandas as pd
import pytest
from deepdiff import DeepDiff

from draco.renderer import AltairRenderer
from draco.renderer.altair.types import MarkType

NUM_ROWS = 100
df = pd.DataFrame(
    {
        "temperature": [random.uniform(1, 44) for _ in range(NUM_ROWS)],
        "wind": [random.uniform(0, 100) for _ in range(NUM_ROWS)],
        "precipitation": [random.uniform(0, 100) for _ in range(NUM_ROWS)],
        "condition": random.choices(
            ["drizzle", "fog", "rain", "sun", "snow"], k=NUM_ROWS
        ),
    }
)


def data(fields):
    return {
        "number_rows": 100,
        "field": [
            x
            for x in [
                {"name": "temperature", "type": "number"},
                {"name": "wind", "type": "number"},
                {"name": "precipitation", "type": "number"},
                {"name": "condition", "type": "string"},
            ]
            if x["name"] in fields
        ],
    }


@pytest.fixture
def renderer():
    return AltairRenderer()


@pytest.fixture
def renderer_with_vconcat():
    return AltairRenderer(concat_mode="vconcat")


@pytest.fixture
def renderer_with_hconcat():
    return AltairRenderer(concat_mode="hconcat")


def vl_specs_equal(a: dict, b: dict) -> bool:
    exclude_from_comparison = {"config", "datasets", "data", "$schema"}
    diff = DeepDiff(
        a,
        b,
        exclude_paths=exclude_from_comparison,
        ignore_order=True,
    )
    return not diff


def build_spec(*args):
    dct = {}
    for arg in args:
        dct.update(arg)
    return dct


def specs_with_mark(mark: MarkType):
    spec_d = build_spec(
        data(["temperature", "wind", "condition"]),
        {
            "view": [
                {
                    "mark": [
                        {
                            "type": mark,
                            "encoding": [
                                {"channel": "x", "field": "temperature"},
                                {"channel": "shape", "field": "condition"},
                                {"channel": "text", "field": "wind"},
                            ],
                        }
                    ],
                    "scale": [{"channel": "x", "type": "linear"}],
                }
            ]
        },
    )
    spec_vl = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
        "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
        "encoding": {
            "x": {
                "field": "temperature",
                "scale": {"type": "linear"},
                "type": "quantitative",
            },
            "shape": {"field": "condition", "type": "nominal"},
            "text": {"field": "wind", "type": "quantitative"},
        },
        "mark": {"type": mark},
    }
    return spec_d, spec_vl


# https://dig.cmu.edu/draco2/facts/examples.html#tick-plot
tick_spec_d = build_spec(
    data(["temperature"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "tick",
                        "encoding": [{"channel": "x", "field": "temperature"}],
                    }
                ],
                "scale": [{"channel": "x", "type": "linear"}],
            }
        ]
    },
)
tick_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        }
    },
    "mark": {"type": "tick"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#tick-plot-with-a-log-scale
tick_log_spec_d = build_spec(
    data(["temperature"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "tick",
                        "encoding": [{"channel": "x", "field": "temperature"}],
                    }
                ],
                "scale": [{"channel": "x", "type": "log"}],
            }
        ]
    },
)
tick_log_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {"field": "temperature", "scale": {"type": "log"}, "type": "quantitative"}
    },
    "mark": {"type": "tick"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#bar-chart
bar_spec_d = build_spec(
    data(["condition", "temperature"]),
    {
        "view": [
            {
                "coordinates": "cartesian",
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {"channel": "x", "field": "condition"},
                            {
                                "channel": "y",
                                "field": "temperature",
                                "aggregate": "mean",
                            },
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "ordinal"},
                    {"channel": "y", "type": "linear", "zero": "true"},
                ],
            }
        ]
    },
)
bar_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {"field": "condition", "type": "ordinal"},
        "y": {
            "aggregate": "mean",
            "field": "temperature",
            "scale": {"type": "linear", "zero": True},
            "type": "quantitative",
        },
    },
    "mark": {"type": "bar"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#histogram
histogram_spec_d = build_spec(
    data(["condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {"channel": "x", "field": "condition"},
                            {"channel": "y", "aggregate": "count"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "ordinal"},
                    {"channel": "y", "type": "linear", "zero": "true"},
                ],
            }
        ]
    },
)
histogram_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {"field": "condition", "type": "ordinal"},
        "y": {
            "aggregate": "count",
            "scale": {"type": "linear", "zero": True},
        },
    },
    "mark": {"type": "bar"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#binned-histogram
binned_histogram_spec_d = build_spec(
    data(["temperature"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {"channel": "x", "field": "temperature", "binning": 10},
                            {"channel": "y", "aggregate": "count"},
                        ],
                    }
                ],
                "scale": [
                    {
                        "channel": "x",
                        "type": "linear",
                    },
                    {"channel": "y", "type": "linear", "zero": "true"},
                ],
            }
        ]
    },
)
binned_histogram_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {
            "bin": {"maxbins": 10},
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {"aggregate": "count", "scale": {"type": "linear", "zero": True}},
    },
    "mark": {"type": "bar"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#scatterplot
scatter_spec_d = build_spec(
    data(["temperature", "wind"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "point",
                        "encoding": [
                            {"channel": "x", "field": "temperature"},
                            {"channel": "y", "field": "wind"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear"},
                    {"channel": "y", "type": "linear"},
                ],
            }
        ]
    },
)
scatter_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
    },
    "mark": {"type": "point"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#scatterplot-with-color
scatter_with_color_spec_d = build_spec(
    data(["temperature", "wind", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "point",
                        "encoding": [
                            {"channel": "x", "field": "temperature"},
                            {"channel": "y", "field": "wind"},
                            {"channel": "color", "field": "condition"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear"},
                    {"channel": "y", "type": "linear"},
                    {"channel": "color", "type": "categorical"},
                ],
            }
        ]
    },
)
scatter_with_color_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "type": "nominal",
        },
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
    },
    "mark": {"type": "point"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#bubble-chart
bubble_spec_d = build_spec(
    data(["temperature", "wind", "precipitation"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "point",
                        "encoding": [
                            {"channel": "x", "field": "temperature"},
                            {"channel": "y", "field": "wind"},
                            {"channel": "size", "field": "precipitation"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear"},
                    {"channel": "y", "type": "linear"},
                    {"channel": "size", "type": "linear"},
                ],
            }
        ]
    },
)
bubble_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "size": {
            "field": "precipitation",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
    },
    "mark": {"type": "point"},
}

marks_to_test: list[MarkType] = ["line", "area", "text", "tick", "rect"]


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (tick_spec_d, tick_spec_vl),
        (tick_log_spec_d, tick_log_spec_vl),
        (bar_spec_d, bar_spec_vl),
        (histogram_spec_d, histogram_spec_vl),
        (binned_histogram_spec_d, binned_histogram_spec_vl),
        (scatter_spec_d, scatter_spec_vl),
        (scatter_with_color_spec_d, scatter_with_color_spec_vl),
        (bubble_spec_d, bubble_spec_vl),
        # Dummy specs for coverage
        *[specs_with_mark(mark) for mark in marks_to_test],
    ],
)
def test_single_view_single_mark(
    spec: dict, expected_vl: dict, renderer: AltairRenderer
):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


# https://dig.cmu.edu/draco2/facts/examples.html#stacked-bar-chart
stacked_bar_spec_d = build_spec(
    data(["temperature", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {"channel": "x", "field": "temperature", "binning": 10},
                            {"channel": "y", "aggregate": "count", "stack": "zero"},
                            {"channel": "color", "field": "condition"},
                        ],
                    }
                ],
                "scale": [
                    {
                        "channel": "x",
                        "type": "linear",
                    },
                    {"channel": "y", "type": "linear", "zero": "true"},
                    {"channel": "color", "type": "categorical"},
                ],
            }
        ]
    },
)
stacked_bar_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "type": "nominal",
        },
        "x": {
            "bin": {"maxbins": 10},
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {
            "aggregate": "count",
            "scale": {"type": "linear", "zero": True},
            "stack": "zero",
        },
    },
    "mark": {"type": "bar"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#normalized-percentage-stacked-bar-chart
normalized_stacked_bar_spec_d = build_spec(
    data(["temperature", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {
                                "channel": "x",
                                "aggregate": "count",
                                "stack": "normalize",
                            },
                            {"channel": "y", "field": "temperature", "binning": 10},
                            {"channel": "color", "field": "condition"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear", "zero": "true"},
                    {"channel": "y", "type": "linear"},
                    {"channel": "color", "type": "categorical"},
                ],
            }
        ]
    },
)
normalized_stacked_bar_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "type": "nominal",
        },
        "x": {
            "aggregate": "count",
            "scale": {"type": "linear", "zero": True},
            "stack": "normalize",
        },
        "y": {
            "bin": {"maxbins": 10},
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
    },
    "mark": {"type": "bar"},
}


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (stacked_bar_spec_d, stacked_bar_spec_vl),
        (normalized_stacked_bar_spec_d, normalized_stacked_bar_spec_vl),
    ],
)
def test_stacked(spec: dict, expected_vl: dict, renderer: AltairRenderer):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


# https://dig.cmu.edu/draco2/facts/examples.html#bar-with-a-tick
bar_with_tick_spec_d = build_spec(
    data(["temperature"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {
                                "channel": "x",
                                "aggregate": "mean",
                                "field": "temperature",
                            }
                        ],
                    },
                    {
                        "type": "tick",
                        "encoding": [{"channel": "x", "field": "temperature"}],
                    },
                ],
                "scale": [{"channel": "x", "type": "linear", "zero": "true"}],
            }
        ]
    },
)
bar_with_tick_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "layer": [
        {
            "encoding": {
                "x": {
                    "aggregate": "mean",
                    "field": "temperature",
                    "scale": {"type": "linear", "zero": True},
                    "type": "quantitative",
                }
            },
            "mark": {"type": "bar"},
        },
        {
            "encoding": {
                "x": {
                    "field": "temperature",
                    "scale": {"type": "linear", "zero": True},
                    "type": "quantitative",
                }
            },
            "mark": {"type": "tick"},
        },
    ],
}


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (bar_with_tick_spec_d, bar_with_tick_spec_vl),
    ],
)
def test_multi_mark(spec: dict, expected_vl: dict, renderer: AltairRenderer):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


# https://dig.cmu.edu/draco2/facts/examples.html#facet-scatterplot-into-columns
scatterplot_columns_spec_d = build_spec(
    data(["temperature", "wind", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "point",
                        "encoding": [
                            {"channel": "x", "field": "temperature"},
                            {"channel": "y", "field": "wind"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear"},
                    {"channel": "y", "type": "linear"},
                ],
                "facet": [
                    {"channel": "col", "field": "condition"},
                ],
            }
        ]
    },
)
scatterplot_columns_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "facet": {"column": {"field": "condition", "type": "nominal"}},
    "spec": {
        "encoding": {
            "x": {
                "field": "temperature",
                "scale": {"type": "linear"},
                "type": "quantitative",
            },
            "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
        },
        "mark": {"type": "point"},
    },
}

scatterplot_rows_spec_d = build_spec(
    data(["temperature", "wind", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "point",
                        "encoding": [
                            {"channel": "x", "field": "temperature"},
                            {"channel": "y", "field": "wind"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "linear"},
                    {"channel": "y", "type": "linear"},
                ],
                "facet": [
                    {"channel": "row", "field": "condition"},
                ],
            }
        ]
    },
)
scatterplot_rows_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "facet": {"row": {"field": "condition", "type": "nominal"}},
    "spec": {
        "encoding": {
            "x": {
                "field": "temperature",
                "scale": {"type": "linear"},
                "type": "quantitative",
            },
            "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
        },
        "mark": {"type": "point"},
    },
}

# https://dig.cmu.edu/draco2/facts/examples.html#facet-scatterplot-by-binned-data-into-columns
scatterplot_columns_binned_spec_d = build_spec(
    data(["temperature", "wind", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "point",
                        "encoding": [
                            {"channel": "x", "field": "condition"},
                            {"channel": "y", "field": "wind"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "ordinal"},
                    {"channel": "y", "type": "linear"},
                ],
                "facet": [
                    {"channel": "col", "field": "temperature", "binning": 10},
                ],
            }
        ]
    },
)
scatterplot_columns_binned_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "facet": {
        "column": {
            "bin": {"maxbins": 10},
            "field": "temperature",
            "type": "quantitative",
        }
    },
    "spec": {
        "encoding": {
            "x": {
                "field": "condition",
                "type": "ordinal",
            },
            "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
        },
        "mark": {"type": "point"},
    },
}


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (scatterplot_columns_spec_d, scatterplot_columns_spec_vl),
        (scatterplot_rows_spec_d, scatterplot_rows_spec_vl),
        (scatterplot_columns_binned_spec_d, scatterplot_columns_binned_spec_vl),
    ],
)
def test_facets(spec: dict, expected_vl: dict, renderer: AltairRenderer):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


# https://dig.cmu.edu/draco2/facts/examples.html#tick-plot-and-histogram
tick_plot_and_histogram_spec_d = build_spec(
    data(["temperature", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "tick",
                        "encoding": [{"channel": "y", "field": "temperature"}],
                    }
                ],
                "scale": [{"channel": "y", "type": "linear", "zero": "true"}],
            },
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {"channel": "x", "field": "condition"},
                            {"channel": "y", "aggregate": "count"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "ordinal"},
                    {"channel": "y", "type": "linear", "zero": "true"},
                ],
            },
        ]
    },
)
tick_plot_and_histogram_spec_base_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "CONCAT_MODE": [
        {
            "encoding": {
                "y": {
                    "field": "temperature",
                    "scale": {"type": "linear", "zero": True},
                    "type": "quantitative",
                }
            },
            "mark": {"type": "tick"},
        },
        {
            "encoding": {
                "x": {
                    "field": "condition",
                    "type": "ordinal",
                },
                "y": {"aggregate": "count", "scale": {"type": "linear", "zero": True}},
            },
            "mark": {"type": "bar"},
        },
    ],
}

# https://dig.cmu.edu/draco2/facts/examples.html#tick-plot-and-histogram-with-shared-y-scale
tick_plot_and_histogram_shared_scale_spec_d = build_spec(
    data(["temperature", "condition"]),
    {
        "view": [
            {
                "mark": [
                    {
                        "type": "tick",
                        "encoding": [{"channel": "y", "field": "temperature"}],
                    }
                ],
            },
            {
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {
                                "channel": "y",
                                "field": "temperature",
                                "aggregate": "mean",
                            },
                            {"channel": "x", "field": "condition"},
                        ],
                    }
                ],
                "scale": [{"channel": "x", "type": "ordinal"}],
            },
        ],
        "scale": [{"channel": "y", "type": "linear", "zero": "true"}],
    },
)
tick_plot_and_histogram_shared_scale_spec_base_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "CONCAT_MODE": [
        {
            "encoding": {"y": {"field": "temperature", "type": "quantitative"}},
            "mark": {"type": "tick"},
        },
        {
            "encoding": {
                "x": {
                    "field": "condition",
                    "type": "ordinal",
                },
                "y": {
                    "aggregate": "mean",
                    "field": "temperature",
                    "type": "quantitative",
                },
            },
            "mark": {"type": "bar"},
        },
    ],
    "resolve": {"scale": {"y": "shared"}},
}


def prepare_multi_view(
    vl_spec: dict, concat_mode: Literal["vconcat", "hconcat"] | None = None
) -> dict:
    result = vl_spec.copy()
    if concat_mode is not None:
        result[concat_mode] = result.pop("CONCAT_MODE")
    else:
        result = result | result.pop("CONCAT_MODE")[0]
    return result


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (
            tick_plot_and_histogram_spec_d,
            prepare_multi_view(tick_plot_and_histogram_spec_base_vl),
        ),
        (
            tick_plot_and_histogram_shared_scale_spec_d,
            prepare_multi_view(tick_plot_and_histogram_shared_scale_spec_base_vl),
        ),
    ],
)
def test_multiple_views_no_concat(
    spec: dict, expected_vl: dict, renderer: AltairRenderer
):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (
            tick_plot_and_histogram_spec_d,
            prepare_multi_view(tick_plot_and_histogram_spec_base_vl, "hconcat"),
        ),
        (
            tick_plot_and_histogram_shared_scale_spec_d,
            prepare_multi_view(
                tick_plot_and_histogram_shared_scale_spec_base_vl, "hconcat"
            ),
        ),
    ],
)
def test_multiple_views_hconcat(
    spec: dict, expected_vl: dict, renderer_with_hconcat: AltairRenderer
):
    chart = renderer_with_hconcat.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (
            tick_plot_and_histogram_spec_d,
            prepare_multi_view(tick_plot_and_histogram_spec_base_vl, "vconcat"),
        ),
        (
            tick_plot_and_histogram_shared_scale_spec_d,
            prepare_multi_view(
                tick_plot_and_histogram_shared_scale_spec_base_vl, "vconcat"
            ),
        ),
    ],
)
def test_multiple_views_vconcat(
    spec: dict, expected_vl: dict, renderer_with_vconcat: AltairRenderer
):
    chart = renderer_with_vconcat.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


def test_unknown_field_raises_value_error(renderer: AltairRenderer):
    spec = build_spec(
        data(["temperature"]),
        {
            "view": [
                {
                    "mark": [
                        {
                            "type": "tick",
                            "encoding": [{"channel": "x", "field": "not-temperature"}],
                        }
                    ],
                    "scale": [{"channel": "x", "type": "linear"}],
                }
            ]
        },
    )
    with pytest.raises(ValueError):
        renderer.render(spec, df)


# https://dig.cmu.edu/draco2/facts/examples.html#pie-chart
polar_pie_chart_spec_d = build_spec(
    data(["condition", "temperature"]),
    {
        "view": [
            {
                "coordinates": "polar",
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {
                                "channel": "y",
                                "aggregate": "count",
                                "stack": "zero",
                            },
                            {"channel": "color", "field": "condition"},
                        ],
                    }
                ],
                "scale": [
                    {"channel": "y", "type": "linear", "zero": "true"},
                    {"channel": "color", "type": "categorical"},
                ],
            }
        ]
    },
)
polar_pie_chart_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "type": "nominal",
        },
        "theta": {
            "aggregate": "count",
            "scale": {"type": "linear", "zero": True},
            "stack": "zero",
        },
    },
    "mark": {"type": "arc"},
}

# https://dig.cmu.edu/draco2/facts/examples.html#radial-chart
polar_radial_chart_spec_d = build_spec(
    data(["condition", "temperature"]),
    {
        "view": [
            {
                "coordinates": "polar",
                "mark": [
                    {
                        "type": "bar",
                        "encoding": [
                            {"channel": "x", "field": "condition"},
                            {
                                "channel": "y",
                                "field": "temperature",
                                "aggregate": "mean",
                            },
                        ],
                    }
                ],
                "scale": [
                    {"channel": "x", "type": "ordinal"},
                    {"channel": "y", "type": "linear", "zero": "true"},
                ],
            }
        ]
    },
)
polar_radial_chart_spec_vl = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
    "config": {
        "view": {"continuousHeight": 300, "continuousWidth": 400},
    },
    "encoding": {
        "radius": {
            "aggregate": "mean",
            "field": "temperature",
            "type": "quantitative",
            "scale": {"type": "linear", "zero": True},
        },
        "text": {"field": "condition", "type": "ordinal"},
        "theta": {
            "field": "condition",
            "type": "ordinal",
        },
    },
    "layer": [
        {"mark": {"type": "arc", "stroke": "#ffffff"}},
        {"mark": {"radiusOffset": 15, "type": "text"}},
    ],
}


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (polar_pie_chart_spec_d, polar_pie_chart_spec_vl),
        (polar_radial_chart_spec_d, polar_radial_chart_spec_vl),
    ],
)
def test_polar(spec: dict, expected_vl: dict, renderer: AltairRenderer):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)
