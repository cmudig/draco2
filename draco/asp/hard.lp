% ====== Hard constraints ======

% @hard(scale_type_data_type) Primitive type has to support scale type.
violation(scale_type_data_type) :-
    attribute((field,type),F,(string;boolean)),
    attribute((encoding,field),E,F),
    helper((encoding,scale_type),E,T),
    domain(continuous_scale,T).

% @hard(log_non_positive) Cannot use log if the data is negative or zero.
violation(log_non_positive) :-
    attribute((field,min),F,MIN),
    attribute((encoding,field),E,F),
    helper((encoding,scale_type),E,log),
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

% @hard(count_without_q) Count has to have a continuous scale.
violation(count_without_q) :-
    attribute((encoding,aggregate),E,count),
    helper((encoding,scale_type),E,T),
    domain(discrete_scale,T).

% @hard(shape_not_ordinal) Shape requires discrete and ordinal (ordinal/categorical doesn't matter as scale types, so we use oridnal only here).
violation(shape_not_ordinal) :-
    helper(mark_scale_channel,_,T,shape),
    T != ordinal.

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

% @hard(encoding_repeat_channel) Cannot use single channels twice for the same mark.
violation(encoding_repeat_channel) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    attribute((encoding,channel),E1,C),
    attribute((encoding,channel),E2,C),
    E1 > E2.

% @hard(scale_repeat_channel) Cannot use single channels twice for the same view.
violation(scale_repeat_channel) :-
    entity(scale,V,S1),
    entity(scale,V,S2),
    attribute((scale,channel),S1,C),
    attribute((scale,channel),S2,C),
    S1 > S2.

% @hard(encoding_channel_without_scale) Encoding channel doesn't have a corresponding scale channel.
violation(encoding_channel_without_scale) :-
    entity(mark,V,M),
    helper((mark,channel),M,C),
    not domain(scale_channel,V,C).

% @hard(scale_channel_without_encoding) Scale channel doesn't have a corresponding encoding channel.
violation(scale_channel_without_encoding) :-
    entity(view,_,V),
    entity(scale,V,S),
    attribute((scale,channel),S,C),
    not domain(encoding_channel,V,C).

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
    not helper((mark,channel),M,text).

% @hard(text_channel_without_text_mark) Text channel requires text mark.
violation(text_channel_without_text_mark) :-
    helper((mark,channel),M,text),
    not attribute((mark,type),M,text).

% @hard(point_tick_bar_without_x_or_y) Point, tick, and bar require x or y channel.
violation(point_tick_bar_without_x_or_y) :-
    attribute((mark,type),M,(point;tick;bar)),
    not helper((mark,channel),M,x),
    not helper((mark,channel),M,y).

% @hard(line_area_without_x_y) Line and area require x and y channel.
violation(line_area_without_x_y) :-
    attribute((mark,type),M,(line;area)),
    { helper((mark,channel),M,x);helper((mark,channel),M,y) } <= 1.

% @hard(line_area_with_discrete) Line and area cannot have both x and y discrete.
violation(line_area_with_discrete) :-
    attribute((mark,type),M,(line;area)),
    helper(mark_scale_channel,M,T1,x),
    helper(mark_scale_channel,M,T2,y),
    domain(discrete_scale,T1),
    domain(discrete_scale,T2).

% @hard(bar_tick_continuous_x_y) Bar and tick cannot have both x and y continuous.
violation(bar_tick_continuous_x_y) :-
    attribute((mark,type),M,(tick;bar)),
    helper(is_c_c,M).

% @hard(view_scale_conflict) A view cannot have a scale definition that conflicts with a shared scale for the same channel.
violation(view_scale_conflict) :-
    entity(view,R,V),
    entity(scale,R,S1),
    entity(scale,V,S2),
    attribute((scale,channel),S1,C),
    attribute((scale,channel),S2,C).

% @hard(shape_without_point) Shape channel requires point mark.
violation(shape_without_point) :-
    helper((mark,channel),M,shape),
    not attribute((mark,type),M,point).

% @hard(size_without_point_text) Size only works with some marks.
violation(size_without_point_text) :-
    helper((mark,channel),M,size),
    not attribute((mark,type),M,text),
    not attribute((mark,type),M,point).

% @hard(detail_without_agg) Detail requires aggregation. Detail adds a field to the group by. Detail could also be used to add information to tooltips. We may remove this later.
violation(detail_without_agg) :-
    entity(encoding,M,E1),
    entity(encoding,M,E2),
    E1 != E2,
    attribute((encoding,channel),E1,detail),
    not attribute((encoding,aggregate),E2,_).

% @hard(area_bar_with_log) Do not use log for bar or area mark as they are often misleading. We may remove this rule in the future.
violation(area_bar_with_log) :-
    attribute((mark,type),M,(bar;area)),
    helper(mark_scale_channel,M,log,(x;y)).

% @hard(rect_without_d_d) Rect mark needs discrete x and y.
violation(rect_without_d_d) :-
    attribute((mark,type),M,rect),
    helper(mark_scale_channel,M,T,(x;y)),
    domain(continuous_scale,T).

% @hard(same_field_x_and_y) Don't use the same field on x and y.
violation(same_field_x_and_y) :-
    helper(mark_channel_field,M,x,F),
    helper(mark_channel_field,M,y,F),
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
    E1 > E2,
    helper((encoding,scale_type),E2,T),
    domain(continuous_scale,T),
    not attribute((encoding,binning),E2,_),
    not attribute((encoding,aggregate),E2,_).

% @hard(detail_not_ordinal) Detail requires ordinal scales.
violation(detail_not_ordinal) :-
    attribute((scale,channel),S,detail),
    not attribute((scale,type),S,ordinal).

% @hard(bar_tick_area_line_without_continuous_x_y) Bar, tick, line, area require some continuous variable on x or y.
violation(bar_tick_area_line_without_continuous_x_y) :-
    attribute((mark,type),M,(bar;tick;area;line)),
    { helper(mark_channel_cont,M,x);helper(mark_channel_cont,M,y) } <= 0.

% @hard(zero_d_n) Can only use zero with datetime or number.
violation(zero_d_n) :-
    helper((mark,scale),M,S),
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    attribute((scale,zero),S,_),
    attribute((scale,channel),S,C),
    attribute((encoding,field),E,F),
    attribute((field,type),F,T),
    T != datetime,
    T != number.

% @hard(bar_area_without_zero) Bar and area mark requires scale of continuous to start at zero.
violation(bar_area_without_zero) :-
    attribute((mark,type),M,(bar;area)),
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    not attribute((encoding,binning),E,_),
    helper((mark,scale),M,S),
    attribute((scale,channel),S,C),
    attribute((scale,type),S,T),
    domain(continuous_scale,T),
    not attribute((scale,zero),S,_),
    C = (x;y).

% @hard(row_no_y) Don't use row without y. Just using y is simpler.
violation(row_no_y) :-
    entity(facet,V,F),
    attribute((facet,channel),F,row),
    entity(mark,V,M),
    not helper((mark,channel),M,y).

% @hard(col_no_x) Don't use column without x. Just using x is simpler.
violation(col_no_x) :-
    entity(facet,V,F),
    attribute((facet,channel),F,col),
    entity(mark,V,M),
    not helper((mark,channel),M,x).

% @hard(stack_without_bar_area) Only use stacking for bar and area.
violation(stack_without_bar_area) :-
    helper(mark_with_stack,M),
    not attribute((mark,type),M,bar),
    not attribute((mark,type),M,area).

% @hard(stack_without_summative_agg) Don't stack if aggregation is not summative (summative are count, sum, distinct, valid, missing).
violation(stack_without_summative_agg) :-
    entity(encoding,_,E),
    attribute((encoding,stack),E,_),
    not attribute((encoding,aggregate),E,sum),
    not attribute((encoding,aggregate),E,count).

% @hard(no_stack_with_bar_area_discrete_color) Need to stack if we use bar, area with discrete color.
violation(no_stack_with_bar_area_discrete_color) :-
    helper(mark_channel_discrete_or_binned,M,color),
    attribute((mark,type),M,(bar;area)),
    not helper(mark_with_stack,M).

% @hard(stack_without_discrete_color_or_detail) Can only use stack if we also use discrete color, or detail.
violation(stack_without_discrete_color_or_detail) :-
    helper(mark_with_stack,M),
    not helper(mark_channel_discrete_or_binned,M,color),
    not helper((mark,channel),M,detail).

% @hard(stack_without_x_y) Stack can only be on x or y.
violation(stack_without_x_y) :-
    attribute((encoding,stack),E,_),
    not attribute((encoding,channel),E,x),
    not attribute((encoding,channel),E,y).

% @hard(stack_discrete) Stack can only be on continuous.
violation(stack_discrete) :-
    attribute((encoding,channel),E,C),
    attribute((encoding,stack),E,_),
    helper(mark_channel_discrete_or_binned,_,C).

% @hard(stack_with_non_positional_non_agg) Cannot use non positional continuous with stack unless it's aggregated.
violation(stack_with_non_positional_non_agg) :-
    helper(mark_with_stack,M),
    entity(encoding,M,E),
    attribute((encoding,channel),E,C),
    domain(non_positional,C),
    not attribute((encoding,aggregate),E,_),
    not helper(mark_channel_discrete_or_binned,M,C).

% @hard(invalid_bin) Check bin type.
violation(invalid_bin) :-
    attribute((encoding,binning),_,B),
    B < 0.

% @hard(invalid_num_rows) number_rows has to be larger than 0.
violation(invalid_num_rows) :-
    attribute(number_rows,root,R),
    R <= 0.

% @hard(invalid_unique) The number of unique values has to be larger than 0.
violation(invalid_unique) :-
    attribute((field,unique),_,U),
    U <= 0.

% @hard(invalid_extent_non_number) Extent only allowed for numbers (for now).
violation(invalid_extent_non_number) :-
    attribute((field,(min;max)),F,_),
    not attribute((field,type),F,number).

% @hard(invalid_non_number_std) Std only allowed for numbers (for now).
violation(invalid_non_number_std) :-
    attribute((field,std),F,_),
    not attribute((field,type),F,number).

% @hard(invalid_std) Std has to be larger or equal to 0.
violation(invalid_std) :-
    attribute((field,std),_,S),
    S < 0.

% @hard(invalid_extent_order) Order has to be correct.
violation(invalid_extent_order) :-
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX),
    MIN > MAX.

% @hard(invalid_non_string_freq) Frequency for strings only.
violation(invalid_non_string_freq) :-
    attribute((field,freq),F,_),
    not attribute((field,type),F,string).
