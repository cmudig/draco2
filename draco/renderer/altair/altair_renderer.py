import logging
import warnings
from dataclasses import dataclass
from typing import Any, Callable, Generic, Literal, TypeVar, cast

import altair as alt
import narwhals as nw

import draco.renderer.utils as renderer_utils
from draco.renderer.base_renderer import BaseRenderer, DataType, LabelMapping

from .types import (
    Encoding,
    EncodingChannel,
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
Used to abstract away the final type of the produced chart instance.
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
    get_label: Callable[[str], str | None]


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

    def __init__(
        self,
        concat_mode: Literal["hconcat", "vconcat"] | None = None,
        mark_config: dict[str, dict[str, Any]] | None = None,
    ):
        """
        Instantiates a new `Altair <https://altair-viz.github.io/>`-based renderer.

        :param concat_mode: The concatenation mode to use
                            when concatenating multiple views.
                            Only the first view is returned if `None`.
        :param mark_config: Optional custom mark configuration.
                            The keys are the mark types, the values are the
                            configuration dictionaries for the mark type.
        """
        self.concat_mode = concat_mode
        self.mark_config = mark_config or {}

    def render(
        self, spec: dict, data: DataType, label_mapping: LabelMapping | None = None
    ) -> VegaLiteChart:
        typed_spec = SpecificationDict.model_validate(spec)
        chart: VegaLiteChart = cast(VegaLiteChart, alt.Chart(data))
        chart_views: list[VegaLiteChart] = []
        data_fields: list[str] = (
            list(data.keys())
            if isinstance(data, dict)
            else nw.from_native(data).columns
        )

        def get_label(field: str) -> str | None:
            if label_mapping is not None:
                return renderer_utils.resolve_label(label_mapping, field)
            return None

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
                        get_label=get_label,
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
                            get_label=get_label,
                        )
                    )
                chart = chart.encode(
                    tooltip=[
                        alt.Tooltip(field, title=get_label(field))
                        for field in data_fields
                    ]
                )
                layers.append(chart)
            chart = self.__visit_view(
                ctx=ViewContext(
                    spec=typed_spec,
                    chart=chart,
                    chart_views=chart_views,
                    layers=layers,
                    view=v,
                    get_label=get_label,
                )
            )
            chart_views.append(chart)

        return self.__visit_root(
            ctx=RootContext(
                spec=typed_spec,
                chart=chart,
                chart_views=chart_views,
                get_label=get_label,
            )
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
            # We collect all facet channels in a single dict so that we can apply them all at once
            facet_channels: dict[str, Any] = {
                "row": alt.Undefined,
                "column": alt.Undefined,
            }
            for f in view.facet:
                channel = f.channel
                title_args = self.__get_title_args(ctx, f.field)
                facet_args: dict[str, Any] = {
                    "field": f.field,
                    "type": self.__find_field_type(ctx.spec, f.field),
                } | title_args
                if f.binning is not None:
                    facet_args["bin"] = alt.BinParams(maxbins=f.binning)
                match channel:
                    case "row":
                        row = alt.Row(**facet_args)
                        facet_channels["row"] = row
                    case "col":
                        column = alt.Column(**facet_args)
                        facet_channels["column"] = column
                    # Should never happen, a pydantic error would be raised sooner
                    case _:  # pragma: no cover
                        raise ValueError(f"Unknown facet channel: {channel}")
            chart = chart.facet(**facet_channels)
            return chart
        return alt.layer(*layers) if len(layers) > 1 else layers[0]  # type: ignore

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

    def __visit_mark_cartesian(self, ctx: MarkContext) -> VegaLiteChart:
        """
        Handles mark-specific configuration.
        Responsible for applying the mark type to a chart in cartesian coordinates.

        :param ctx: The current visitor context.
        :return: The chart with the mark applied.
        :raises ValueError: if the mark type is not supported
        """
        chart, mark_type = (ctx.chart, ctx.mark.type)
        mark_config = self.mark_config.get(mark_type, {})
        match mark_type:
            case "point":
                return chart.mark_point(**mark_config)
            case "bar":
                return chart.mark_bar(**mark_config)
            case "line":
                return chart.mark_line(**mark_config)
            case "area":
                return chart.mark_area(**mark_config)
            case "text":
                return chart.mark_text(**mark_config)
            case "tick":
                return chart.mark_tick(**mark_config)
            case "rect":
                return chart.mark_rect(**mark_config)

        # Should never happen, a pydantic error would be raised sooner
        raise ValueError(f"Unknown mark type: {mark_type}")  # pragma: no cover

    def __visit_mark_polar(self, ctx: MarkContext) -> VegaLiteChart:
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
                    return chart.mark_arc(
                        stroke="#ffffff",
                        **self.mark_config.get("arc", {}),
                    ) + chart.mark_text(
                        radiusOffset=15,
                        **self.mark_config.get("text", {}),
                    )
                else:
                    return chart.mark_arc()
            # Should never happen, a pydantic error would be raised sooner
            case _:  # pragma: no cover
                raise ValueError(f"Unknown mark type: {mark_type}")

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
        field_type = renderer_utils.find_raw_field_type(spec.field, encoding.field)
        custom_args: dict[str, Any] = {}
        if encoding.field is not None:
            custom_args["field"] = encoding.field
            custom_args["type"] = self.__find_field_type(spec, encoding.field)
        if encoding.binning is not None:
            custom_args["bin"] = alt.BinParams(maxbins=encoding.binning)

        # TODO(peter-gy): move `seconds_span_to_vegalite_time_unit` to utils and expose its params via renderer ctor
        # TODO(peter-gy): revise how we compute temporal cadence: if we have only yearly data it does not make sense to include anything other than year. We need more than just `span_seconds` to know this.
        if field_type == "datetime":
            if fieldname := ctx.encoding.field:
                field = renderer_utils.find_field_by_name(spec.field, fieldname)
                if field.span_seconds is not None:
                    custom_args["timeUnit"] = seconds_span_to_vegalite_time_unit(
                        field.span_seconds,
                        level=1,
                    )

        # TODO(peter-gy): extend ASP core to reason about field sorting
        if field_type in {"string"}:
            if encoding.channel == "x":
                custom_args["sort"] = "-y"
            elif encoding.channel == "y":
                custom_args["sort"] = "-x"

        if view.scale is not None:
            scale_or_none = self.__find_alt_scale_for_encoding(
                field_type, mark.type, encoding.channel, view.scale
            )
            if scale_or_none is not None:
                custom_args["scale"] = scale_or_none

        title_args = self.__get_title_args(ctx, encoding.field)
        encoding_args = (
            encoding.model_dump(
                exclude_none=True, exclude={"channel", "field", "binning"}
            )
            | custom_args
            | title_args
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

        custom_args: dict[str, Any] = {}
        if encoding.field is not None:
            custom_args["field"] = encoding.field
            custom_args["type"] = self.__find_field_type(spec, encoding.field)

        if view.scale is not None:
            field_type = renderer_utils.find_raw_field_type(spec.field, encoding.field)
            scale_or_none = self.__find_alt_scale_for_encoding(
                field_type, mark.type, encoding.channel, view.scale
            )
            if scale_or_none is not None:
                custom_args["scale"] = scale_or_none

        title_args = self.__get_title_args(ctx, encoding.field)
        encoding_args = (
            encoding.model_dump(
                exclude_none=True, exclude={"channel", "field", "binning", "scale"}
            )
            | custom_args
            | title_args
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
            case _:  # pragma: no cover
                raise ValueError(f"Unknown channel: {encoding.channel}")

    @staticmethod
    def __find_field_type(spec: SpecificationDict, field_name: FieldName) -> str:
        """
        Returns the type of the field with the given name.
        Needed to map from Draco-spec data types to Vega-Lite data types.
        Also takes the scale's type into account which is associated with the field.

        :param spec: the whole specification
        :param field_name: name of the field to look up
        :return: the type of the field
        """
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
            "symlog": {
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

        field = renderer_utils.find_field_by_name(spec.field, field_name)
        # Look for the encoding channel of the field, so we can match it to a scale
        channel = renderer_utils.find_encoding_channel_of_field(spec.view, field_name)
        # We might have no channel in case of a faceted field
        # --> we map based on the raw data type
        if channel is None:
            return renames[__DEFAULT_KEY__][field.type]

        # Look for the scale associated with `channel`
        scales_of_spec = renderer_utils.find_scales_of_spec(spec)
        scale = renderer_utils.find_scale_for_encoding(channel, scales_of_spec)
        # We might have no scale present for the channel
        # --> we map based on the raw data type
        key = scale.type if scale is not None else __DEFAULT_KEY__
        return renames[key][field.type]

    @staticmethod
    def __find_alt_scale_for_encoding(
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
        scale = renderer_utils.find_scale_for_encoding(channel, scales)
        if scale is None:
            return None

        # Extract arguments and process them further
        scale_args = scale.model_dump(exclude_none=True, exclude={"channel"})

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

    @staticmethod
    def __get_title_args(ctx: RootContext, field: FieldName | None) -> dict[str, Any]:
        if field is None:
            return {}
        label = ctx.get_label(field)
        if label is None:
            return {}
        return {"title": label}


def seconds_span_to_vegalite_time_unit(
    span_seconds: int,
    utc: bool = False,
    hierarchical: bool = True,
    level: int | None = None,
    binned: bool = False,
) -> str:
    """
    Convert a time span in seconds to the most appropriate Vega-Lite time unit.

    Supports hierarchical time units (e.g., 'yearmonthdate') for better temporal granularity
    when dealing with larger time spans that benefit from multiple levels of detail.

    :param span_seconds: The time span in seconds
    :param utc: Whether to use UTC time units (adds 'utc' prefix)
    :param hierarchical: Whether to use hierarchical time units (e.g., 'yearmonthdate' instead of just 'year')
    :param level: Limit hierarchical depth (1=single unit, 2=two units, etc.). None means no limit.
    :param binned: Whether to add 'binned' prefix for chronological time units
    :return: The appropriate Vega-Lite time unit string

    Examples:
        - seconds_span_to_vegalite_time_unit(3600) -> "hours"
        - seconds_span_to_vegalite_time_unit(31536000, hierarchical=True) -> "yearmonthdate"
        - seconds_span_to_vegalite_time_unit(31536000, level=2) -> "yearmonth"
        - seconds_span_to_vegalite_time_unit(3600, utc=True, binned=True) -> "binnedhours"
    """
    # Define time unit thresholds in seconds
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY  # Approximate
    QUARTER = 3 * MONTH  # Approximate
    YEAR = 365 * DAY  # Approximate

    # Hierarchical time unit combinations based on span
    hierarchical_units = {
        "milliseconds": ["milliseconds"],
        "seconds": ["seconds"],
        "minutes": ["minutes", "seconds"],
        "hours": ["hours", "minutes"],
        "day": ["day", "hours"],
        "week": ["week", "day"],
        "month": ["month", "date"],
        "quarter": ["quarter", "month"],
        "year": ["year", "month", "date"],
        "multi_year": ["year", "month", "date", "hours"],
    }

    # Determine base time unit
    if span_seconds < 1:
        base_unit = "milliseconds"
    elif span_seconds < MINUTE:
        base_unit = "seconds"
    elif span_seconds < HOUR:
        base_unit = "minutes"
    elif span_seconds < DAY:
        base_unit = "hours"
    elif span_seconds < WEEK:
        base_unit = "day"
    elif span_seconds < MONTH:
        base_unit = "week"
    elif span_seconds < QUARTER:
        base_unit = "month"
    elif span_seconds < YEAR:
        base_unit = "quarter"
    elif span_seconds < 5 * YEAR:
        base_unit = "year"
    else:
        base_unit = "multi_year"

    # Get time unit components
    if hierarchical:
        units = hierarchical_units[base_unit].copy()

        # Apply level limitation if specified
        if level is not None:
            if level <= 0:
                units = []  # Empty list for level 0 or negative
            else:
                units = units[:level]

        # Create hierarchical time unit string
        time_unit = "".join(units)
    else:
        # Use only the primary unit
        if base_unit == "multi_year":
            time_unit = "year"
        elif base_unit == "day":
            time_unit = "date"  # Use 'date' for calendar days in non-hierarchical mode
        else:
            time_unit = hierarchical_units[base_unit][0]

    # Add prefixes
    prefixes = []
    if binned and base_unit not in [
        "milliseconds",
        "seconds",
        "minutes",
    ]:  # Binned prefix for chronological units
        prefixes.append("binned")
    if utc:
        prefixes.append("utc")

    prefix = "".join(prefixes)

    return f"{prefix}{time_unit}"
