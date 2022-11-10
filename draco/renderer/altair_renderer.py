from dataclasses import dataclass
from typing import Generic, TypeVar

import altair as alt
from pandas import DataFrame

from ..types import (
    Encoding,
    EncodingChannel,
    Field,
    FieldName,
    Mark,
    Scale,
    SpecificationDict,
    View,
)
from .base_renderer import BaseRenderer

"""
Generic parameter for the type of the produced visualization object.
Used to abstract away the final type of the produced visualization object.
"""
VegaLiteChart = TypeVar(
    "VegaLiteChart", alt.VConcatChart, alt.HConcatChart, alt.FacetChart, alt.Chart
)


@dataclass(frozen=True)
class RootContext(Generic[VegaLiteChart]):
    """
    Visitor callback context available when processing
    the dictionary-based specification at the root level.
    """

    spec: SpecificationDict
    chart: VegaLiteChart
    chart_views: list[VegaLiteChart]


@dataclass(frozen=True)
class ViewContext(RootContext):
    """
    Visitor callback context available when processing
    the dictionary-based specification at the `View` level.
    """

    view: View


@dataclass(frozen=True)
class MarkContext(ViewContext):
    """
    Visitor callback context available when processing
    the dictionary-based specification at the `Mark` level.
    """

    mark: Mark


@dataclass(frozen=True)
class EncodingContext(MarkContext):
    """
    Visitor callback context available when processing
    the dictionary-based specification at the `Encoding` level.
    """

    encoding: Encoding


class AltairRenderer(BaseRenderer[VegaLiteChart]):
    """
    Produces a `Vega-Lite <https://vega.github.io/vega-lite/>`_ visualization
    represented as an `Altair <https://altair-viz.github.io/>`_ chart object.
    """

    def render(self, spec: SpecificationDict, data: DataFrame) -> VegaLiteChart:
        # initial chart to be mutated by the visitor callbacks
        chart = alt.Chart(data)
        chart_views: list[VegaLiteChart] = []

        # Traverse the specification dict and invoke the appropriate visitor
        for v in spec.view:
            for m in v.mark:
                chart = self.__visit_mark(
                    ctx=MarkContext(
                        spec=spec, chart=chart, chart_views=chart_views, view=v, mark=m
                    )
                )
                for e in m.encoding:
                    chart = self.__visit_encoding(
                        ctx=EncodingContext(
                            spec=spec,
                            chart=chart,
                            chart_views=chart_views,
                            view=v,
                            mark=m,
                            encoding=e,
                        )
                    )
            chart = self.__visit_view(
                ctx=ViewContext(spec=spec, chart=chart, chart_views=chart_views, view=v)
            )
            chart_views.append(chart)
        return self.__visit_root(
            ctx=RootContext(spec=spec, chart=chart, chart_views=chart_views)
        )

    def __visit_root(self, ctx: RootContext) -> VegaLiteChart:
        """
        Handles root-level configuration.
        Responsible for chart concatenation and resolution of shared axes.

        :param ctx: The current visitor context.
        :return: The chart with the root configuration applied.
        """
        views = ctx.chart_views
        chart = len(views) > 1 and alt.vconcat(*views) or views[0]
        if ctx.spec.scale is not None:
            channels = [s.channel for s in ctx.spec.scale]
            resolve_scale_args = {c: "shared" for c in channels}
            chart = chart.resolve_scale(**resolve_scale_args)
        return chart

    def __visit_view(self, ctx: ViewContext) -> VegaLiteChart:
        """
        Handles view-specific configuration.
        Responsible for faceting and concatenation.

        :param ctx: The current visitor context.
        :return: The chart with the view applied.
        :raises ValueError: if the facet channel is not supported
        """
        view, chart = (ctx.view, ctx.chart)
        if view.facet is not None:
            for f in view.facet:
                channel = f.channel
                facet_args = {
                    "field": f.field,
                    "type": self.__get_field_type(ctx.spec.field, f.field),
                }
                if f.binning is not None:
                    facet_args["bin"] = alt.BinParams(maxbins=f.binning)
                match channel:
                    case "row":
                        chart = chart.facet(row=alt.Row(**facet_args))
                    case "col":
                        chart = chart.facet(column=alt.Column(**facet_args))
                    case _:
                        raise ValueError(f"Unknown facet channel: {channel}")
        return chart

    def __visit_mark(self, ctx: MarkContext) -> VegaLiteChart:
        """
        Handles mark-specific configuration.
        Responsible for applying the mark type to the chart.

        :param ctx: The current visitor context.
        :return: The chart with the mark applied.
        :raises ValueError: if the mark type is not supported
        """
        chart, mark_type = (ctx.chart, ctx.mark.type)
        match mark_type:
            case "point":
                return chart.mark_point()
            case "bar":
                return chart.mark_bar()
            case "line":
                return chart.mark_line()
            case "area":
                return chart.mark_area()
            case "text":
                return chart.mark_text()
            case "tick":
                return chart.mark_tick()
            case "rect":
                return chart.mark_rect()
            case _:
                raise ValueError(f"Unknown mark type: {mark_type}")

    def __visit_encoding(self, ctx: EncodingContext) -> VegaLiteChart:
        """
        Handles encoding-specific configuration.
        Responsible for applying the encoding to the chart.

        :param ctx: The current visitor context.
        :return: The updated chart.
        :raises ValueError: If an unknown encoding channel is encountered.
        """
        spec, chart, view, encoding = (ctx.spec, ctx.chart, ctx.view, ctx.encoding)

        custom_args = {}
        if encoding.field is not None:
            custom_args["field"] = encoding.field
            custom_args["type"] = self.__get_field_type(spec.field, encoding.field)
        if encoding.binning is not None:
            custom_args["bin"] = alt.BinParams(maxbins=encoding.binning)

        if view.scale is not None:
            scale_or_none = self.__get_scale_for_encoding(encoding.channel, view.scale)
            if scale_or_none is not None:
                custom_args["scale"] = scale_or_none

        encoding_args = (
            encoding.dict(exclude_none=True, exclude={"channel", "field", "binning"})
            | custom_args
        )

        match encoding.channel:
            case "x":
                return chart.encode(x=alt.X(**encoding_args))
            case "y":
                return chart.encode(y=alt.Y(**encoding_args))
            case "color":
                return chart.encode(color=alt.Color(**encoding_args))
            case "size":
                return chart.encode(size=alt.Size(**encoding_args))
            case "shape":
                return chart.encode(shape=alt.Shape(**encoding_args))
            case "text":
                return chart.encode(text=alt.Text(**encoding_args))
            case _:
                raise ValueError(f"Unknown channel: {encoding.channel}")

    def __get_field_type(self, fields: list[Field], field_name: FieldName) -> str:
        """
        Returns the type of the field with the given name.
        Needed to map from Draco-spec data types to Vega-Lite data types.

        :param fields: list of fields in the specification
        :param field_name: name of the field to look up
        :return: the type of the field
        :raises ValueError: if the field is not found
        """
        renames = {
            "number": "quantitative",
            "string": "nominal",
            "boolean": "nominal",
            "datetime": "temporal",
        }
        field_by_name = [f for f in fields if f.name == field_name]
        if len(field_by_name) == 0:
            raise ValueError(f"Unknown field: {field_name}")
        return renames[field_by_name[0].type]

    def __get_scale_for_encoding(
        self, channel: EncodingChannel, scales: list[Scale]
    ) -> alt.Scale | None:
        """
        Returns the scale for the given encoding channel, if any.

        :param channel: the channel for which to look up a scale
        :param scales: the list of scales in the view
        :return: the scale for the given channel, or None if no scale is found
        """
        renames = {
            "categorical": "ordinal",
        }
        for scale in scales:
            if scale.channel == channel:
                scale_args = scale.dict(exclude_none=True, exclude={"channel"})
                scale_args["type"] = renames.get(scale.type, scale.type)
                return alt.Scale(**scale_args)
        return None
