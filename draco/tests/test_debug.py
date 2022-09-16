from typing import Iterable

import pytest

from draco.debug import DracoDebug

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


@pytest.mark.parametrize(
    "feature_names, weights",
    [
        (None, None),
        ({"polar_coordinate", "summary_discrete"}, None),
        (None, {"polar_coordinate_weight": 5, "summary_discrete_weight": 10}),
        (
            {"polar_coordinate", "summary_discrete", "summary_discrete_y"},
            {"polar_coordinate_weight": 5, "summary_discrete_weight": 10},
        ),
    ],
)
def test_init(feature_names, weights):
    instance = DracoDebug(specs=specs, feature_names=feature_names, weights=weights)
    feature_keys = set(
        f"{feature_name}_weight" for feature_name in instance.feature_names
    )
    weight_keys = set(instance.weights.keys())
    # After init, each feature should have a weight associated with it
    assert feature_keys == weight_keys


def test_chart_preferences():
    instance = DracoDebug(specs=specs)
    df = instance.chart_preferences
    rows, cols = df.shape
    assert cols == 4
    assert rows == len(instance.specs) * len(instance.feature_names)
