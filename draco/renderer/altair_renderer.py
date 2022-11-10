from dataclasses import dataclass
from typing import TypeVar

import altair as alt
from pandas import DataFrame

from ..types import (
    Encoding,
    EncodingChannel,
    Field,
    FieldName,
    Mark,
    SpecificationDict,
    View,
)
from .base_renderer import BaseRenderer

VegaLiteChart = TypeVar("VegaLiteChart", alt.VConcatChart, alt.HConcatChart, alt.Chart)


@dataclass(frozen=True)
class VisitorContext:
    spec: SpecificationDict
    product: VegaLiteChart
    views: list[View] | None = None
    view: View | None = None
    mark: Mark | None = None
    encoding: Encoding | None = None


class AltairRenderer(BaseRenderer[VegaLiteChart]):
    def build(self, spec: SpecificationDict, data: DataFrame) -> VegaLiteChart:
        chart = alt.Chart(data)
        views = []
        for v in spec.view:
            for m in v.mark:
                chart = self.__visit_mark(
                    ctx=VisitorContext(
                        spec=spec, product=chart, views=views, view=v, mark=m
                    )
                )
                for e in m.encoding:
                    chart = self.__visit_encoding(
                        ctx=VisitorContext(
                            spec=spec,
                            product=chart,
                            views=views,
                            view=v,
                            mark=m,
                            encoding=e,
                        )
                    )
            chart = self.__visit_view(
                ctx=VisitorContext(spec=spec, product=chart, views=views, view=v)
            )
            views.append(chart)
        return self.__visit_root(
            ctx=VisitorContext(spec=spec, product=chart, views=views)
        )

    def display(self, product: VegaLiteChart) -> None:
        pass

    def __visit_root(self, ctx: VisitorContext) -> VegaLiteChart:
        views = ctx.views
        chart = len(views) > 1 and alt.vconcat(*views) or views[0]
        has_shared_scale = ctx.spec.scale is not None
        if has_shared_scale:
            channels = [s.channel for s in ctx.spec.scale]
            resolve_scale_args = {c: "shared" for c in channels}
            chart = chart.resolve_scale(**resolve_scale_args)
        return chart

    def __visit_view(self, ctx: VisitorContext) -> VegaLiteChart:
        view, chart = (ctx.view, ctx.product)
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

    def __visit_mark(self, ctx: VisitorContext) -> VegaLiteChart:
        chart, mark_type = (ctx.product, ctx.mark.type)
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

    def __visit_encoding(self, ctx: VisitorContext) -> VegaLiteChart:
        spec, chart, view, encoding = (ctx.spec, ctx.product, ctx.view, ctx.encoding)

        custom_args = {}
        if encoding.field is not None:
            custom_args["field"] = encoding.field
            custom_args["type"] = self.__get_field_type(spec.field, encoding.field)
        if encoding.binning is not None:
            custom_args["bin"] = alt.BinParams(maxbins=encoding.binning)

        if view.scale is not None:
            scale_or_none = self.__get_scale_for_encoding(encoding.channel, view)
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
        self, channel: EncodingChannel, view: View
    ) -> alt.Scale | None:
        renames = {
            "categorical": "ordinal",
        }
        for scale in view.scale:
            if scale.channel == channel:
                scale_args = scale.dict(exclude_none=True, exclude={"channel"})
                scale_args["type"] = renames.get(scale.type, scale.type)
                return alt.Scale(**scale_args)
        return None
