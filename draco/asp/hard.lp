% ====== Hard constraints ======

% @hard(enc_type_valid) Primitive type has to support data type.
violation(enc_type_valid) :-
    attribute(field_type,N,(string;boolean)),
    attribute(scale_type,M,C,T),
    attribute(channel_field,M,C,N),
    T != ordinal,
    T != categorical.

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
    attribute(scale_type,M,C,(ordinal;categorical)),
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

% @hard(aggregate_detail) Detail cannot be aggregated.
violation(aggregate_detail) :-
    attribute((encoding,channel),E,detail),
    attribute((encoding,aggregate),E,_).

% @hard(count_without_field) Count cannot use a field.
violation(count_without_field) :-
    attribute((encoding,field),E,_),
    attribute((encoding,aggregate),E,count).

% @hard(count_without_q) Count has to have a quantitative scale.
violation(count_without_q) :-
    attribute((encoding,aggregate),E,count),
    attribute((encoding,type),E,T),
    T != log,
    T != linear.

% @hard(categorical_not_color) Categorical only applied to color channel.
violation(categorical_not_color) :-
    attribute((scale,type),S,categorical),
    not attribute((scale,channel),S,color).

% @hard(size_negative) Do not use size when data is negative as size implies that data is positive.
violation(size_negative) :-
    attribute((encoding,channel),E,size),
    attribute((encoding,field),E,N),
    attribute(extent,N,MIN,MAX),
    MIN < 0,
    MAX > 0.

% @hard(repeat_channel) Cannot use single channels twice for the same mark.
violation(repeat_channel) :-
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
    not attribute(mark_channel,M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    attribute(mark_channel,M,text),
    not attribute((mark,type),M,text).

% @hard(point_tick_bar_without_x_or_y) Point, tick, and bar require x or y channel.
violation(point_tick_bar_without_x_or_y) :-
    attribute((mark,type),M,(point;tick;bar)),
    not attribute(mark_channel,M,x),
    not attribute(mark_channel,M,y).

% @hard(line_area_without_x_y) Line and area require x and y channel.
violation(line_area_without_x_y) :-
    attribute((mark,type),M,(line;area)),
    {attribute(mark_channel,M,x);attribute(mark_channel,M,y)} <= 1.

% @hard(line_area_with_discrete) Line and area cannot have two discrete(ie. x and y cannot both be discrete).
violation(line_area_with_discrete) :-
    attribute((mark,type),M,(line;area)),
    attribute(discrete,M,x),
    attribute(discrete,M,y).

% @hard(bar_tick_continuous_x_y) Bar and tick cannot have both x and y continuous.
violation(bar_tick_continuous_x_y) :-
    attribute((mark,type),M,(tick;bar)),
    attribute(continuous,M,x),
    attribute(continuous,M,y).