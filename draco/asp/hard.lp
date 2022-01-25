% ====== Hard constraints ======

% === Within Encodings ===

% @hard(bin_and_aggregate) Cannot bin and aggregate.
violation(bin_and_aggregate) :-
    attribute((encoding,binning),E,_),
    attribute((encoding,aggregate),E,_).

% === Across encodings and between encodings and marks ===

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
    entity(encoding,_,E),
    attribute((mark,type),E,(point;tick;bar)),
    not attribute((encoding,channel),E,x),
    not attribute((encoding,channel),E,y).

% === Global properties ===



% == Stacking ==

% @hard(stack_without_bar_area) Only use stacking for bar and area.
violation(stack_without_bar_area) :-
    attribute(has_stack,M),
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
    attribute((mark,type),M,(bar;area)),
    attribute(has_discrete_color,M),
    not attribute(has_stack,M).

% @hard(stack_without_discrete_color_or_detail) Can only use stack if we also use discrete color, or detail.
violation(stack_without_discrete_color_or_detail) :-
    attribute(has_stack,M),
    not attribute(has_channel,M,detail),
    not attribute(has_discrete_color,M).


% @hard(stack_detail_without_q_color) If we use stack and detail, we also have to use quantitative color.
violation(stack_detail_without_q_color) :-
    attribute(has_stack,M),
    attribute(has_channel,M,detail),
    not attribute(has_channel,M,color).

% @hard(stack_detail_without_q_color_2) If we use stack and detail, we also have to use quantitative color.
violation(stack_detail_without_q_color_2) :-
    attribute(has_stack,M),
    attribute(has_channel,M,detail),
    entity(encoding,M,E),
    attribute((encoding,channel),E,color),
    not attribute((encoding,aggregate),E,_).

% @hard(stack_discrete) Stack can only be on continuous.
violation(stack_discrete) :-
    attribute((encoding,stack),E,_),
    attribute(discrete,E).

% @hard(stack_without_x_y) Stack can only be on x or y.
violation(stack_without_x_y) :-
    attribute((encoding,stack),E,_),
    not attribute((encoding,channel),E,x),
    not attribute((encoding,channel),E,y).

% @hard(stack_with_non_positional_non_agg) Cannot use non positional continuous with stack unless it's aggregated.
violation(stack_with_non_positional_non_agg) :-
    attribute(has_stack,M),
    attribute(encoding,M,E),
    attribute((encoding,channel),E,C),
    domain(non_positional,C),
    not attribute((encoding,aggregate),E,_),
    not attribute(discrete,E).

% @hard(shape_with_cardinality_gt_eight) Vega-Lite currently supports 8 shapes.
violation(shape_with_cardinality_gt_eight) :-
    entity(field,root,F),
    attribute((field,unique),F,U),
    attribute((encoding,channel),C,shape),
    attribute((encoding,field),C,F),
    U > 8.

% @hard(color_with_cardinality_gt_twenty) At most 20 categorical colors.
violation(color_with_cardinality_gt_twenty) :-
    entity(field,root,F),
    attribute((field,unique),F,U),
    attribute((encoding,channel),E,color),
    attribute((encoding,field),C,F),
    attribute((scale,channel),S,color),
    attribute((scale,type),S,(ordinal;nominal)),
    U > 20.

% === Type checks ===

% @hard(invalid_mark) Check mark.
violation(invalid_mark) :-
    attribute((mark,type),_,M),
    not domain((mark,type),M).

% @hard(invalid_channel) Check channel.
violation(invalid_channel) :-
    attribute((encoding,channel),_,C),
    not domain(single_channel,C),
    not domain(multi_channel,C).

% @hard(invalid_field_name) Check field name.
violation(invalid_field_name) :-
    attribute((encoding,field),_,F),
    not domain((field,name),F).

% @hard(invalid_scale) Check scale type.
violation(invalid_scale) :-
    attribute((scale,type),_,S),
    not domain((scale,type),S).

% @hard(invalid_aggregate) Check aggregate type.
violation(invalid_aggregate) :-
    attribute((encoding,aggregate),_,A),
    not domain((encoding,aggregate),A).

% @hard(invalid_bin) Check bin type.
violation(invalid_bin) :-
    attribute((encoding,binning),_,B),
    not B >= 0.

% @hard(invalid_field_type) Check field type.
violation(invalid_field_type) :-
    attribute((field,type),_,F),
    not domain((field,type),F).

% @hard(invalid_task) Task has to be one of the tasks.
violation(invalid_task) :-
    attribute(task,root,T),
    not domain(task,T).

% @hard(invalid_num_rows) Num_rows has to be larger than 0.
violation(invalid_num_rows) :-
    attribute(number_rows,root,R),
    R <= 0.

% @hard(invalid_unique) The number of unique values has to be larger than 0.
violation(invalid_unique) :-
    attribute((field,unique),_,U),
    U <= 0.

% @hard(invalid_extent_non_number_min) Extent only allowed for numbers (for now).
violation(invalid_extent_non_number_min) :-
    attribute((field,min),F,_),
    not attribute((field,type),F,number).

% @hard(invalid_extent_non_number_max) Extent only allowed for numbers (for now).
violation(invalid_extent_non_number_max) :-
    attribute((field,max),F,_),
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

% @hard(encoding_field_same_name) The name of a field cannot be the name of an encoding. This is to prevent errors coming from the shortcuts in define.lp.
violation(encoding_field_same_name) :-
    attribute((field,name),0,F),
    domain(channel,F).