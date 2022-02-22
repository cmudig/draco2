% ====== Hard constraints ======

% @hard(scale_type_data_type) Primitive type has to support scale type.
violation(scale_type_data_type) :-
    attribute((field,type),F,(string;boolean)),
    attribute((encoding,field),E,F),
    attribute((encoding,scale_type),E,T),
    domain(continuous_scale,T).

% @hard(log_non_positive) Cannot use log if the data is negative or zero.
violation(log_non_positive) :-
    attribute((field,min),F,MIN),
    attribute((encoding,field),E,F),
    attribute((encoding,scale_type),E,log),
    MIN <= 0.

% @hard(bin_and_aggregate) Cannot bin and aggregate.
violation(bin_and_aggregate) :-
    attribute((encoding,binning),E,_),
    attribute((encoding,aggregate),E,_).

% @hard(aggregate_t_valid) Temporal scale only supports min and max.
violation(aggregate_t_valid) :-
    attribute((field,type),F,datetime),
    attribute((encoding,field),E,F),
    attribute((encoding,aggregate),E,A),
    A != min,
    A != max.

% @hard(aggregate_num_valid) Only numbers can be aggregated with mean, sum, stdev
violation(aggregate_num_valid) :-
    attribute((field,type),F,T),
    attribute((encoding,field),E,F),
    attribute((encoding,aggregate),E,(mean;sum;stdev)),
    T != number.

% @hard(bin_n_d) Only numbers and datetimes can be binned
violation(bin_n_d) :-
    attribute((field,type),F,T),
    attribute((encoding,field),E,F),
    attribute((encoding,binning),E,_),
    T != number,
    T != datetime.

% @hard(aggregate_detail) Detail cannot be aggregated.
violation(aggregate_detail) :-
    attribute((encoding,channel),E,detail),
    attribute((encoding,aggregate),E,_).

% @hard(count_without_field) Count cannot use a field.
violation(count_without_field) :-
    attribute((encoding,field),E,_),
    attribute((encoding,aggregate),E,count).

% @hard(count_without_q) Count has to have a continuous scale.
violation(count_without_q) :-
    attribute((encoding,aggregate),E,count),
    attribute((encoding,scale_type),E,T),
    domain(discrete_scale,T).

% @hard(categorical_not_color) Categorical only works with color channel.
violation(categorical_not_color) :-
    attribute((scale,type),S,categorical),
    not attribute((scale,channel),S,color).

% @hard(size_negative) Do not use size when data is negative as size implies that data is positive.
violation(size_negative) :-
    attribute((encoding,channel),E,size),
    attribute((encoding,field),E,F),
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX),
    MIN < 0,
    MAX > 0.

% @hard(repeat_channel) Cannot use single channels twice for the same mark.
violation(repeat_channel) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,C),
    attribute((encoding,channel),E2,C),
    E1 > E2.

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
    not attribute((mark,channel),M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    attribute((mark,channel),M,text),
    not attribute((mark,type),M,text).

% @hard(point_tick_bar_without_x_or_y) Point, tick, and bar require x or y channel.
violation(point_tick_bar_without_x_or_y) :-
    attribute((mark,type),M,(point;tick;bar)),
    not attribute((mark,channel),M,x),
    not attribute((mark,channel),M,y).

% @hard(line_area_without_x_y) Line and area require x and y channel.
violation(line_area_without_x_y) :-
    attribute((mark,type),M,(line;area)),
    { attribute((mark,channel),M,x);attribute((mark,channel),M,y) } <= 1.

% @hard(line_area_with_discrete) Line and area cannot have both x and y discrete.
violation(line_area_with_discrete) :-
    attribute((mark,type),M,(line;area)),
    attribute(mark_scale_channel,M,T1,x),
    attribute(mark_scale_channel,M,T2,y),
    domain(discrete_scale,T1),
    domain(discrete_scale,T2).


% @hard(bar_tick_continuous_x_y) Bar and tick cannot have both x and y continuous.
violation(bar_tick_continuous_x_y) :-
    attribute((mark,type),M,(tick;bar)),
    attribute(mark_scale_channel,M,T1,x),
    attribute(mark_scale_channel,M,T2,y),
    domain(continuous_scale,T1),
    domain(continuous_scale,T2).

% @hard(view_scale_conflict) A view cannot have a scale definition that conflicts with a shared scale for the same channel.
violation(view_scale_conflict) :-
    entity(view,R,V),
    entity(scale,R,S1),
    entity(scale,V,S2),
    attribute((scale,channel),S1,C),
    attribute((scale,channel),S2,C).

% @hard(shape_without_point) Shape channel requires point mark.
violation(shape_without_point) :-
    attribute((mark,channel),M,shape),
    not attribute((mark,type),M,point).

% @hard(size_without_point_text) Size only works with some marks.
violation(size_without_point_text) :-
    attribute((mark,channel),M,size),
    not attribute((mark,type),M,text),
    not attribute((mark,type),M,point).

% @hard(detail_without_agg) Detail requires aggregation. Detail adds a field to the group by. Detail could also be used to add information to tooltips. We may remove this later.
violation(detail_without_agg) :-
    attribute((encoding,channel),E,detail),
    not attribute((encoding,aggregate),E,_).

% @hard(area_bar_with_log) Do not use log for bar or area mark as they are often misleading. We may remove this rule in the future.
violation(area_bar_with_log) :-
    attribute((mark,type),M,(bar;area)),
    attribute(mark_scale_channel,M,log,(x;y)).

% @hard(rect_without_d_d) Rect mark needs discrete x and y.
violation(rect_without_d_d) :-
    attribute((mark,type),M,rect),
    attribute(mark_scale_channel,M,T,(x;y)),
    domain(continuous_scale,T).

% @hard(same_field_x_and_y) Don't use the same field on x and y.
violation(same_field_x_and_y) :-
    { attribute(mark_channel_field,M,x,F);attribute(mark_channel_field,M,y,F) } >= 2,
    entity(field,root,F),
    entity(mark,_,M).

% @hard(count_twice) Don't use count twice.
violation(count_twice):-
    { entity(encoding,M,E) : attribute((encoding,aggregate),E,count) } >= 2,
    entity(mark,_,M).

% @hard(aggregate_not_all_continuous) If we use aggregation, then all continuous scales need to be aggregated.
violation(aggregate_not_all_continuous):-
    attribute((encoding,aggregate),E1,_),
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,scale_type),E2,T),
    domain(continuous_scale,T),
    not attribute((encoding,aggregate),E2,_).
