% ====== Field Control ======

% @api(require(field, fieldname)) Guarantee that a field is visualized via encoding or facet
violation(field_not_visualized) :-
    require(field, FieldName),
    not attribute((encoding,field),_,FieldName),
    not attribute((facet,field),_,FieldName).

% @api(require((field, encoding), fieldname)) Guarantee that a specific field is used in an encoding
violation(field_not_in_encoding) :-
    require((field, encoding), FieldName),
    not attribute((encoding,field),_,FieldName).

% @api(require((field, facet), fieldname)) Guarantee that a specific field is used in a facet
violation(field_not_in_facet) :-
    require((field, facet), FieldName),
    not attribute((facet,field),_,FieldName).

% @api(forbid(field, fieldname)) Forbid a field from being used in any visualization
violation(forbidden_field_used) :-
    forbid(field, FieldName),
    attribute((encoding,field),_,FieldName).

violation(forbidden_field_used) :-
    forbid(field, FieldName),
    attribute((facet,field),_,FieldName).

% @api(observed(field, fieldname)) Field is used (in encoding or facet)
observed(field, FieldName) :-
    attribute((encoding,field),_,FieldName).

observed(field, FieldName) :-
    attribute((facet,field),_,FieldName).

% @api(observed((field, encoding), fieldname)) Field is used in an encoding
observed((field, encoding), FieldName) :-
    attribute((encoding,field),_,FieldName).

% @api(observed((field, facet), fieldname)) Field is used in a facet
observed((field, facet), FieldName) :-
    attribute((facet,field),_,FieldName).

% ====== Mark Control ======

% @api(require(mark, marktype)) Guarantee that a specific mark type is used
violation(required_mark_missing) :-
    require(mark, MarkType),
    not attribute((mark,type),_,MarkType).

% @api(forbid(mark, marktype)) Forbid a specific mark type from being used
violation(forbidden_mark_used) :-
    forbid(mark, MarkType),
    attribute((mark,type),_,MarkType).

% @api(observed(mark, marktype)) Mark type is used
observed(mark, MarkType) :-
    attribute((mark,type),_,MarkType).

% ====== Channel Control ======

% @api(require(channel, channelname)) Guarantee that a specific channel is used
violation(required_channel_missing) :-
    require(channel, Channel),
    not attribute((encoding,channel),_,Channel).

% @api(forbid(channel, channelname)) Forbid a specific channel from being used
violation(forbidden_channel_used) :-
    forbid(channel, Channel),
    attribute((encoding,channel),_,Channel).

% @api(observed(channel, channelname)) Channel is used
observed(channel, Channel) :-
    attribute((encoding,channel),_,Channel).

% ====== Facet Control ======

% @api(require(facet)) Guarantee that faceting is used
violation(faceting_missing) :-
    require(facet),
    not entity(facet,_,_).

% @api(forbid(facet)) Forbid any faceting
violation(faceting_forbidden) :-
    forbid(facet),
    entity(facet,_,_).

% @api(require((facet, channel), channelname)) Require faceting on a specific channel (row/col)
violation(facet_channel_missing) :-
    require((facet, channel), Channel),
    not attribute((facet,channel),_,Channel).

% @api(forbid((facet, channel), channelname)) Forbid faceting on a specific channel
violation(facet_channel_forbidden) :-
    forbid((facet, channel), Channel),
    attribute((facet,channel),_,Channel).

% @api(observed(facet)) Faceting is used
observed(facet) :-
    entity(facet,_,_).

% @api(observed((facet, channel), channelname)) Specific facet channel is used
observed((facet, channel), Channel) :-
    attribute((facet,channel),_,Channel).

% ====== Binning Control ======

% @api(require(binning)) Guarantee that at least one encoding uses binning
violation(binning_missing) :-
    require(binning),
    not attribute((encoding,binning),_,_).

% @api(forbid(binning)) Forbid any binning
violation(binning_forbidden) :-
    forbid(binning),
    attribute((encoding,binning),_,_).

% @api(require(binning, fieldname)) Require a specific field to be binned
violation(field_not_binned) :-
    require(binning, FieldName),
    attribute((encoding,field),E,FieldName),
    not attribute((encoding,binning),E,_).

% @api(forbid(binning, fieldname)) Forbid a specific field from being binned
violation(field_binned_forbidden) :-
    forbid(binning, FieldName),
    attribute((encoding,field),E,FieldName),
    attribute((encoding,binning),E,_).

% @api(observed(binning)) Binning is used
observed(binning) :-
    attribute((encoding,binning),_,_).

% @api(observed(binning, fieldname)) Specific field is binned
observed(binning, FieldName) :-
    attribute((encoding,field),E,FieldName),
    attribute((encoding,binning),E,_).

% ====== Aggregation Control ======

% @api(require(aggregate)) Guarantee that at least one encoding uses aggregation
violation(aggregation_missing) :-
    require(aggregate),
    not attribute((encoding,aggregate),_,_).

% @api(forbid(aggregate)) Forbid any aggregation
violation(aggregation_forbidden) :-
    forbid(aggregate),
    attribute((encoding,aggregate),_,_).

% @api(require(aggregate, aggtype)) Require a specific aggregation type to be used
violation(required_aggregate_missing) :-
    require(aggregate, AggType),
    not attribute((encoding,aggregate),_,AggType).

% @api(forbid(aggregate, aggtype)) Forbid a specific aggregation type
violation(forbidden_aggregate_used) :-
    forbid(aggregate, AggType),
    attribute((encoding,aggregate),_,AggType).

% @api(observed(aggregate)) Aggregation is used
observed(aggregate) :-
    attribute((encoding,aggregate),_,_).

% @api(observed(aggregate, aggtype)) Specific aggregation type is used
observed(aggregate, AggType) :-
    attribute((encoding,aggregate),_,AggType).

% ====== Scale Control ======

% @api(require(scale, scaletype)) Require a specific scale type to be used
violation(required_scale_missing) :-
    require(scale, ScaleType),
    not attribute((scale,type),_,ScaleType).

% @api(forbid(scale, scaletype)) Forbid a specific scale type
violation(forbidden_scale_used) :-
    forbid(scale, ScaleType),
    attribute((scale,type),_,ScaleType).

% @api(require((scale, channel), scaletype)) Require a specific scale type for a specific channel
violation(required_channel_scale_missing) :-
    require((scale, Channel), ScaleType),
    entity(scale,_,S),
    attribute((scale,channel),S,Channel),
    not attribute((scale,type),S,ScaleType).

% @api(forbid((scale, channel), scaletype)) Forbid a specific scale type for a specific channel
violation(forbidden_channel_scale_used) :-
    forbid((scale, Channel), ScaleType),
    entity(scale,_,S),
    attribute((scale,channel),S,Channel),
    attribute((scale,type),S,ScaleType).

% @api(observed(scale, scaletype)) Scale type is used
observed(scale, ScaleType) :-
    attribute((scale,type),_,ScaleType).

% @api(observed((scale, channel), scaletype)) Specific scale type used on specific channel
observed((scale, Channel), ScaleType) :-
    entity(scale,_,S),
    attribute((scale,channel),S,Channel),
    attribute((scale,type),S,ScaleType).

% ====== Stack Control ======

% @api(require(stack)) Guarantee that stacking is used
violation(stacking_missing) :-
    require(stack),
    not attribute((encoding,stack),_,_).

% @api(forbid(stack)) Forbid any stacking
violation(stacking_forbidden) :-
    forbid(stack),
    attribute((encoding,stack),_,_).

% @api(require(stack, stackmethod)) Require a specific stacking method
violation(required_stack_method_missing) :-
    require(stack, StackMethod),
    not attribute((encoding,stack),_,StackMethod).

% @api(forbid(stack, stackmethod)) Forbid a specific stacking method
violation(forbidden_stack_method_used) :-
    forbid(stack, StackMethod),
    attribute((encoding,stack),_,StackMethod).

% @api(observed(stack)) Stacking is used
observed(stack) :-
    attribute((encoding,stack),_,_).

% @api(observed(stack, stackmethod)) Specific stack method is used
observed(stack, StackMethod) :-
    attribute((encoding,stack),_,StackMethod).

% ====== Definition Declarations ======
% Tell Clingo these predicates are defined externally to silence "atom does not occur in any rule head" warnings.

#defined require/1.
#defined require/2.
#defined forbid/1.
#defined forbid/2.
