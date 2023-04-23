from pandas import DataFrame

from draco.renderer import AltairRenderer


def render_spec(spec: dict) -> dict:
    data = DataFrame()
    chart = AltairRenderer().render(spec=spec, data=data)
    return chart.to_dict()
