from pandas import DataFrame

from draco.renderer import AltairRenderer


def render_spec(spec: dict) -> dict:
    """
    Renders a draco specification to a Vega-Lite specification
    using the :code:`AltairRenderer` with an empty `DataFrame`.

    :returns: Vega-Lite specification as a dictionary
    """
    data = DataFrame()
    chart = AltairRenderer().render(spec=spec, data=data)
    return chart.to_dict()
