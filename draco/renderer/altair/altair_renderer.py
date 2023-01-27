import logging
import warnings
from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

import altair as alt
from pandas import DataFrame

from draco.renderer.base_renderer import BaseRenderer

from .types import (
    Encoding,
    EncodingChannel,
    Field,
    FieldName,
    FieldType,
    Mark,
    MarkType,
    Scale,
    SpecificationDict,
    View,
)

logger = logging.getLogger(__name__)

"""
Generic parameter for the type of the produced visualization object.
Used to abstract away the final type of the produced visualization object.
"""
VegaLiteChart = TypeVar(
    "VegaLiteChart",
    alt.VConcatChart,
    alt.HConcatChart,
    alt.FacetChart,
    alt.Chart,
    alt.LayerChart,
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
class ViewContext(RootContext[VegaLiteChart]):
    """
    Visitor callback context available when processing
    the dictionary-based specification at the `View` level.
    """

    layers: list[VegaLiteChart]
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

    def __init__(self, concat_mode: Literal["hconcat", "vconcat"] | None = None):
        """
        Instantiates a new `Altair <https://altair-viz.github.io/>`-based renderer.

        :param concat_mode: The concatenation mode to use
                            when concatenating multiple views.
                            Only the first view is returned if `None`.
        """
        self.concat_mode = concat_mode

    def render(self, spec: dict, data: DataFrame) -> VegaLiteChart:
        typed_spec = SpecificationDict.parse_obj(spec)
        # initial chart to be mutated by the visitor callbacks
        chart = alt.Chart(data)
        chart_views: list[VegaLiteChart] = []

        # Traverse the specification dict and invoke the appropriate visitor
        for v in typed_spec.view:
            layers: list[VegaLiteChart] = []
            for m in v.mark:
                chart = self.__visit_mark(
                    ctx=MarkContext(
                        spec=typed_spec,
                        chart=chart,
                        chart_views=chart_views,
                        layers=layers,
                        view=v,
                        mark=m,
                    )
                )
                for e in m.encoding:
                    chart = self.__visit_encoding(
                        ctx=EncodingContext(
                            spec=typed_spec,
                            chart=chart,
                            chart_views=chart_views,
                            layers=layers,
                            view=v,
                            mark=m,
                            encoding=e,
                        )
                    )
                layers.append(chart)
            chart = self.__visit_view(
                ctx=ViewContext(
                    spec=typed_spec,
                    chart=chart,
                    chart_views=chart_views,
                    layers=layers,
                    view=v,
                )
            )
            chart_views.append(chart)
        return self.__visit_root(
            ctx=RootContext(spec=typed_spec, chart=chart, chart_views=chart_views)
        )

    def __visit_root(self, ctx: RootContext) -> VegaLiteChart:
        """
        Handles root-level configuration.
        Responsible for chart concatenation and resolution of shared axes.

        :param ctx: The current visitor context.
        :return: The chart with the root configuration applied.
        """
        views = ctx.chart_views
        chart = views[0]
        is_multi_view = len(views) > 1

        # TODO: move this logic to the ASP layer by introducing constraints
        if is_multi_view:
            if self.concat_mode is not None:
                chart = getattr(alt, self.concat_mode)(*views)
            else:
                warnings.warn(
                    message="No concatenation performed on multiple views. "
                    "Returning the first view."
                )

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
        view, chart, layers = (ctx.view, ctx.chart, ctx.layers)
        if view.facet is not None:
            for f in view.facet:
                channel = f.channel
                facet_args = {
                    "field": f.field,
                    "type": self.__get_field_type(ctx.spec, f.field),
                }
                if f.binning is not None:
                    facet_args["bin"] = alt.BinParams(maxbins=f.binning)
                match channel:
                    case "row":
                        chart = chart.facet(row=alt.Row(**facet_args))
                    case "col":
                        chart = chart.facet(column=alt.Column(**facet_args))
                    # Should never happen, a pydantic error would be raised sooner
                    case _:  # pragma: no cover
                        raise ValueError(
                            f"Unknown facet channel: {channel}"
                        )  # pragma: no cover
            return chart
        return alt.layer(*layers) if len(layers) > 1 else layers[0]

    def __visit_mark(self, ctx: MarkContext) -> VegaLiteChart:
        """
        Handles mark-specific configuration.
        Responsible for applying the mark type to the chart.

        :param ctx: The current visitor context.
        :return: The chart with the mark applied.
        :raises ValueError: if the coordinate type is not supported
        """
        coord = ctx.view.coordinates
        match coord:
            case "cartesian":
                return self.__visit_mark_cartesian(ctx)
            case "polar":
                return self.__visit_mark_polar(ctx)

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown coordinate type: {coord}")  # pragma: no cover

    @staticmethod
    def __visit_mark_cartesian(ctx: MarkContext) -> VegaLiteChart:
        """
        Handles mark-specific configuration.
        Responsible for applying the mark type to a chart in cartesian coordinates.

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

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown mark type: {mark_type}")  # pragma: no cover

    @staticmethod
    def __visit_mark_polar(ctx: MarkContext) -> VegaLiteChart:
        """
        Handles mark-specific configuration.
        Responsible for applying the mark type to a chart in polar coordinates.

        :param ctx: The current visitor context.
        :return: The chart with the mark applied.
        :raises ValueError: if the mark type is not supported
        """
        chart, encodings, mark_type = (ctx.chart, ctx.mark.encoding, ctx.mark.type)
        match mark_type:
            case "bar":
                encodes_x_and_y = all([e.channel in ["x", "y"] for e in encodings])
                if encodes_x_and_y:
                    # We are setting a white stroke here so that the radial
                    # slices are visually separated from each other.
                    # See https://github.com/cmudig/draco2/pull/438#discussion_r1042469389  # noqa: E501
                    return chart.mark_arc(stroke="#ffffff") + chart.mark_text(
                        radiusOffset=15
                    )
                else:
                    return chart.mark_arc()

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown mark type: {mark_type}")  # pragma: no cover

    def __visit_encoding(self, ctx: EncodingContext) -> VegaLiteChart:
        """
        Handles encoding-specific configuration.
        Responsible for applying the encoding to the chart.

        :param ctx: The current visitor context.
        :return: The updated chart.
        :raises ValueError: If an unknown encoding channel is encountered.
        """
        coord = ctx.view.coordinates
        match coord:
            case "cartesian":
                return self.__visit_encoding_cartesian(ctx)
            case "polar":
                return self.__visit_encoding_polar(ctx)

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown coordinate type: {coord}")  # pragma: no cover

    def __visit_encoding_cartesian(self, ctx: EncodingContext) -> VegaLiteChart:
        """
        Handles encoding-specific configuration.
        Responsible for applying the encoding to a chart in cartesian coordinates.

        :param ctx: The current visitor context.
        :return: The updated chart.
        :raises ValueError: If an unknown encoding channel is encountered.
        """
        spec, chart, view, mark, encoding = (
            ctx.spec,
            ctx.chart,
            ctx.view,
            ctx.mark,
            ctx.encoding,
        )
        custom_args = {}
        if encoding.field is not None:
            custom_args["field"] = encoding.field
            custom_args["type"] = self.__get_field_type(spec, encoding.field)
        if encoding.binning is not None:
            custom_args["bin"] = alt.BinParams(maxbins=encoding.binning)

        if view.scale is not None:
            field_type = self.__get_field_type_raw(spec.field, encoding.field)
            scale_or_none = self.__get_alt_scale_for_encoding(
                field_type, mark.type, encoding.channel, view.scale
            )
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

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown channel: {encoding.channel}")  # pragma: no cover

    def __visit_encoding_polar(self, ctx: EncodingContext) -> VegaLiteChart:
        """
        Handles encoding-specific configuration.
        Responsible for applying the encoding to a chart in polar coordinates.

        :param ctx: The current visitor context.
        :return: The updated chart.
        :raises ValueError: If an unknown encoding channel is encountered.
        """
        spec, chart, view, mark, encoding, encodings = (
            ctx.spec,
            ctx.chart,
            ctx.view,
            ctx.mark,
            ctx.encoding,
            ctx.mark.encoding,
        )
        encodes_x_and_y = all([e.channel in ["x", "y"] for e in encodings])

        custom_args = {}
        if encoding.field is not None:
            custom_args["field"] = encoding.field
            custom_args["type"] = self.__get_field_type(spec, encoding.field)

        if view.scale is not None:
            field_type = self.__get_field_type_raw(spec.field, encoding.field)
            scale_or_none = self.__get_alt_scale_for_encoding(
                field_type, mark.type, encoding.channel, view.scale
            )
            if scale_or_none is not None:
                custom_args["scale"] = scale_or_none

        encoding_args = (
            encoding.dict(
                exclude_none=True, exclude={"channel", "field", "binning", "scale"}
            )
            | custom_args
        )

        match encoding.channel:
            case "x":
                return chart.encode(
                    theta=alt.Theta(**encoding_args),
                    text=alt.Text(
                        field=encoding_args["field"], type=encoding_args["type"]
                    ),
                )
            case "y":
                if encodes_x_and_y:
                    return chart.encode(radius=alt.Radius(**encoding_args))
                else:
                    return chart.encode(theta=alt.Theta(**encoding_args))
            case "color":
                return chart.encode(color=alt.Color(**encoding_args))

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown channel: {encoding.channel}")  # pragma: no cover

    @staticmethod
    def __get_encoding_channel_of_field(
        views: list[View], field_name: FieldName
    ) -> EncodingChannel | None:
        """
        Returns the mark encoding channel for the field with the given name.

        :param views: All the views in the spec to search for.
        :param field_name: The name of the field to search for.
        :return: The encoding channel of the field, or `None` if
                 the field is not found.
        """
        for v in views:
            for m in v.mark:
                for e in m.encoding:
                    if e.field == field_name:
                        return e.channel

        return None

    @staticmethod
    def __get_scales_of_spec(spec: SpecificationDict) -> list[Scale]:
        """
        Returns all the scales in the spec including the top-level
        shared scale and the view-specific scales.

        :param spec: The spec to search through for scales.
        :return: A list of all the scales in the spec.
        """
        scales: list[Scale] = []

        # Shared scales
        for s in spec.scale or []:
            scales.append(s)

        # View-specific scales
        for v in spec.view:
            for s in v.scale or []:
                scales.append(s)

        return scales

    @staticmethod
    def __get_field_by_name(fields: list[Field], field_name: FieldName) -> Field:
        """
        Returns the field with the given name.

        :param fields: The list of fields to search through.
        :param field_name: The name of the field to search for.
        :return: The field with the given name.
        :raises ValueError: If the field is not found.
        """
        for f in fields:
            if f.name == field_name:
                return f

        raise ValueError(f"Field {field_name} not found")

    @staticmethod
    def __get_field_type(spec: SpecificationDict, field_name: FieldName) -> str:
        """
        Returns the type of the field with the given name.
        Needed to map from Draco-spec data types to Vega-Lite data types.
        Also takes the scale's type into account which is associated with the field.

        :param spec: the whole specification
        :param field_name: name of the field to look up
        :return: the type of the field
        """
        cls = AltairRenderer
        __DEFAULT_KEY__ = "default"
        # Multi-criteria lookup to determine the type of the field
        # based on the scale type (if any) AND the raw data type.
        renames = {
            "linear": {
                "number": "quantitative",
                "datetime": "temporal",
            },
            "log": {
                "number": "quantitative",
                "datetime": "quantitative",
            },
            "ordinal": {
                "number": "ordinal",
                "string": "ordinal",
                "boolean": "ordinal",
                "datetime": "ordinal",
            },
            "categorical": {
                "number": "nominal",
                "string": "nominal",
                "boolean": "nominal",
                "datetime": "nominal",
            },
            __DEFAULT_KEY__: {
                "number": "quantitative",
                "string": "nominal",
                "boolean": "nominal",
                "datetime": "temporal",
            },
        }

        field = cls.__get_field_by_name(spec.field, field_name)
        # Look for the encoding channel of the field, so we can match it to a scale
        channel = cls.__get_encoding_channel_of_field(spec.view, field_name)
        # We might have no channel in case of a faceted field
        # --> we map based on the raw data type
        if channel is None:
            return renames[__DEFAULT_KEY__][field.type]

        # Look for the scale associated with `channel`
        scale = cls.__get_scale_for_encoding(channel, cls.__get_scales_of_spec(spec))
        # We might have no scale present for the channel
        # --> we map based on the raw data type
        key = scale.type if scale is not None else __DEFAULT_KEY__
        return renames[key][field.type]

    @staticmethod
    def __get_scale_for_encoding(
        channel: EncodingChannel, scales: list[Scale]
    ) -> Scale | None:
        """
        Returns the `Scale` for the given encoding channel, if any.

        :param channel: the channel for which to look up a scale
        :param scales: the list of scales in the view
        :return: the scale for the given channel, or None if no scale is found
        """
        for scale in scales:
            if scale.channel == channel:
                return scale
        return None

    @staticmethod
    def __get_field_type_raw(
        fields: list[Field], field_name: FieldName | None
    ) -> FieldType:
        if field_name is None:
            return "number"

        cls = AltairRenderer
        field_type = cls.__get_field_by_name(fields, field_name)
        return field_type.type

    @staticmethod
    def __get_alt_scale_for_encoding(
        field_type: FieldType,
        mark_type: MarkType,
        channel: EncodingChannel,
        scales: list[Scale],
    ) -> alt.Scale | None:
        """
        Returns an `alt.Scale` for the given encoding channel, if any.

        :param field_type: the type of the field for which to look up a scale
        :param mark_type: the type of the mark used for the field
        :param channel: the channel for which to look up a scale
        :param scales: the list of scales in the view
        :return: the scale for the given channel, or None if no scale is found
        """
        scale = AltairRenderer.__get_scale_for_encoding(channel, scales)
        if scale is None:
            return None

        # Extract arguments and process them further
        scale_args = scale.dict(exclude_none=True, exclude={"channel"})

        renames = {
            "categorical": "ordinal",
        }

        alt_scale_type = renames.get(scale.type, scale.type)

        # Whenever we have a scale specified other than "ordinal",
        # we assign it to the args explicitly.
        if alt_scale_type is not None and alt_scale_type != "ordinal":
            scale_args["type"] = alt_scale_type
        else:
            # Otherwise, we remove the type from the args,
            # so that Vega-Lite can infer it automatically.
            del scale_args["type"]

        return alt.Scale(**scale_args) if scale_args else None
