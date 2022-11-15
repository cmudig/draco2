import random

import pandas as pd
import pytest
from deepdiff import DeepDiff

from draco.renderer import AltairRenderer
from draco.types import SpecificationDict

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
    return SpecificationDict.parse_obj(dct)


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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        }
    },
    "mark": "tick",
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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {"field": "temperature", "scale": {"type": "log"}, "type": "quantitative"}
    },
    "mark": "tick",
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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {"field": "condition", "scale": {"type": "ordinal"}, "type": "nominal"},
        "y": {
            "aggregate": "mean",
            "field": "temperature",
            "scale": {"type": "linear", "zero": True},
            "type": "quantitative",
        },
    },
    "mark": "bar",
}

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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {"field": "condition", "scale": {"type": "ordinal"}, "type": "nominal"},
        "y": {
            "aggregate": "count",
            "scale": {"type": "linear", "zero": True},
        },
    },
    "mark": "bar",
}

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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
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
    "mark": "bar",
}

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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
    },
    "mark": "point",
}

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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "scale": {"type": "ordinal"},
            "type": "nominal",
        },
        "x": {
            "field": "temperature",
            "scale": {"type": "linear"},
            "type": "quantitative",
        },
        "y": {"field": "wind", "scale": {"type": "linear"}, "type": "quantitative"},
    },
    "mark": "point",
}

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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
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
    "mark": "point",
}


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
    ],
)
def test_single_view_single_mark(
    spec: SpecificationDict, expected_vl: dict, renderer: AltairRenderer
):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)


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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "type": "nominal",
            "scale": {"type": "ordinal"},
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
    "mark": "bar",
}

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
    "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
    "config": {"view": {"continuousHeight": 300, "continuousWidth": 400}},
    "encoding": {
        "color": {
            "field": "condition",
            "type": "nominal",
            "scale": {"type": "ordinal"},
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
    "mark": "bar",
}


@pytest.mark.parametrize(
    "spec, expected_vl",
    [
        (stacked_bar_spec_d, stacked_bar_spec_vl),
        (normalized_stacked_bar_spec_d, normalized_stacked_bar_spec_vl),
    ],
)
def test_stacked(spec: SpecificationDict, expected_vl: dict, renderer: AltairRenderer):
    chart = renderer.render(spec, df)
    vl = chart.to_dict()
    assert vl_specs_equal(vl, expected_vl)
