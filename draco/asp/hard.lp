% ====== Hard constraints ======

% @hard(enc_type_valid) Primitive type has to support data type.
violation(enc_type_valid) :-
    attribute(field_type,N,(string;boolean)),
    attribute(scale_type,M,C,T),
    attribute(channel_field,M,C,N),
    T != ordinal.

% @hard(bin_q_o) Can only bin quantitative or ordinal.
violation(bin_q_o) :-
    attribute(scale_type,M,C,T),
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,binning),E,_),
    T != linear,
    T != log,
    T != ordinal.

% @hard(log_non_positive) Cannot use log if the data is negative or zero.
violation(log_non_positive) :-
    attribute(extent,N,MIN,_),
    attribute(channel_field,M,C,N),
    attribute(scale_type,M,C,log),
    MIN <= 0.

% @hard(bin_and_aggregate) Cannot bin and aggregate.
violation(bin_and_aggregate) :-
    attribute((encoding,binning),E,_),
    attribute((encoding,aggregate),E,_).

% @hard(aggregate_o_valid) Oridnal only supports min, max, and median.
violation(aggregate_o_valid) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,aggregate),E,A),
    attribute(scale_type,M,C,ordinal),
    A != min,
    A != max,
    A != median.

% @hard(aggregate_t_valid) Temporal only supports min and max.
violation(aggregate_t_valid) :-
    attribute(field_type,N,datetime),
    attribute((encoding,field),E,N),
    attribute((encoding,aggregate),E,A),
    A != min,
    A != max.

% @hard(aggregate_nominal) Cannot aggregate categorical.
violation(aggregate_nominal) :-
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((encoding,aggregate),E,_),
    attribute(scale_type,M,C,categorical).

% @hard(aggregate_detail) Detail cannot be aggregated.
violation(aggregate_detail) :-
    attribute((encoding,channel),E,detail),
    attribute((encoding,aggregate),E,_).

% @hard(count_q_without_field) Count has to be quantitative and not use a field.
violation(count_q_without_field) :-
    attribute((encoding,field),E,_),
    attribute((encoding,aggregate),E,count).
violation(count_q_without_field) :-
    entity(encoding,M,E),
    attribute((encoding,aggregate),E,count),
    attribute((encoding,channel),E,C),
    attribute(scale_type,M,C,T),
    T != linear,
    T != log.

% @hard(shape_discrete_non_ordered) Shape requires discrete and not ordered (nominal). Using ordinal would't make a difference in Vega-Lite.
violation(shape_discrete_non_ordered) :-
    attribute((scale,channel),E,shape),
    not attribute((scale,type),E,categorical).

% @hard(detail_non_ordered) Detail requires nominal.
violation(detail_non_ordered) :-
    attribute((scale,channel),E,detail),
    not attribute((scale,type),E,categorical).

% @hard(size_nominal)  Size implies order so nominal is misleading.
violation(size_nominal) :-
    attribute((scale,channel),E,size),
    attribute((scale,type),E,categorical).

% @hard(size_negative) Do not use size when data is negative as size implies that data is positive.
violation(size_negative) :-
    attribute(channel_field,_,size,N),
    attribute(extent,N,MIN,MAX),
    MIN < 0,
    MAX > 0.

% @hard(repeat_channel) Cannot use single channels twice for the same mark.
violation(repeat_channel) :-
    entity(mark,_,M),
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,C),
    attribute((encoding,channel),E2,C),
    E1 != E2.

% @hard(no_encodings) There has to be at least one encoding for every mark.
violation(no_encodings) :-
    entity(mark,_,M),
    not entity(encoding,M,_).

% @hard(encoding_no_field_and_not_count) All encodings (if they have a channel) require field except if we have a count aggregate.
violation(encoding_no_field_and_not_count) :-
    entity(encoding,_,E),
    not attribute((encoding,field),E,_),
    not attribute((encoding,aggregate),E,count).

% @hard(count_with_field) Count should not have a field. Having a field doesn't make a difference.
violation(count_with_field) :-
    attribute((encoding,aggregate),E,count),
    attribute((encoding,field),E,_).

% @hard(text_mark_without_text_channel) Text mark requires text encoding.
violation(text_mark_without_text_channel) :-
    attribute((mark,type),M,text),
    not attribute(has_channel,M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    not attribute((mark,type),M,text),
    attribute(has_channel,M,text).

% @hard(point_tick_bar_without_x_or_y) Point, tick, and bar require x or y channel.
violation(point_tick_bar_without_x_or_y) :-
    entity(mark,_,M),
    entity(encoding,M,E),
    attribute((mark,type),M,(point;tick;bar)),
    not attribute((encoding,channel),E,x),
    not attribute((encoding,channel),E,y).

% @hard(line_area_without_x_y) Line and area require x and y channel.
violation(line_area_without_x_y) :-
    entity(mark,_,M),
    attribute((mark,type),M,(line;area)),
    not attribute(has_x_y_channels,M).

% @hard(line_area_with_discrete) Line and area cannot have two discrete(ie. x and y cannot both be discrete).
violation(line_area_with_discrete) :-
    attribute((mark,type),M,(line;area)),
    attribute(discrete,M,x),
    attribute(discrete,M,y).

% @hard(bar_tick_continuous_x_y) Bar and tick cannot have both x and y continuous.
violation(bar_tick_continuous_x_y) :-
    entity(mark,_,M),
    attribute((mark,type),M,(tick;bar)),
    attribute(has_cont_channel,M,x),
    attribute(has_cont_channel,M,y).