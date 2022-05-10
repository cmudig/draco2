% ====== Preferences ======

% @soft(aggregate) Prefer to use raw (no aggregate).
preference(aggregate,E) :-
    attribute((encoding,aggregate),E,_).

% @soft(bin) Prefer to not bin.
preference(bin,E) :-
    attribute((encoding,binning),E,_).

% @soft(bin_high) Prefer binning with at most 12 buckets.
preference(bin_high,E) :-
    attribute((encoding,binning),E,B), B > 12.

% @soft(bin_low) Prefer binning with more than 7 buckets.
preference(bin_low,E) :-
    attribute((encoding,binning),E,B), B <= 7.

% @soft(encoding) Prefer to use fewer encodings.
preference(encoding,E) :-
    entity(encoding,_,E).

% @soft(encoding_field) Prefer to use fewer encodings with fields (count does not have a field).
preference(encoding_field,E) :-
    attribute((encoding,field),E,_).

% @soft(same_field) Prefer not to use the same field twice for the same mark.
preference(same_field,F) :-
    entity(field,_,F),
    entity(mark,_,M),
    { entity(encoding,M,E): attribute((encoding,field),E,F) } = 2.

% @soft(same_field_grt3) Prefer not to use the same field three or more times for the same mark.
preference(same_field_grt3,F) :-
    entity(field,_,F),
    entity(mark,_,M),
    { entity(encoding,M,E): attribute((encoding,field),E,F) } >= 3.

% @soft(count_grt1) Prefer not to use count more than once.
preference(count_grt1,M) :-
    entity(mark,_,M),
    { entity(encoding,M,E): attribute((encoding,aggregate),E,count) } > 1.

% @soft(number_categorical) Should not use categorical scale for number field.
preference(number_categorical,E) :-
    attribute((field,type),F,number),
    attribute((encoding,field),E,F),
    attribute((encoding,scale_type),E,categorical).

% @soft(bin_low_unique) Binned field should not have too less unique values.
preference(bin_low_unique,E) :-
    attribute((field,type),F,(number;datetime)),
    attribute((field,unique),F,U),
    attribute((encoding,field),E,F),
    attribute((encoding,binning),E,_),
    U < 15.

% @soft(bin_not_linear) Prefer linear scale for bin.
preference(bin_not_linear,E) :-
    attribute((encoding,binning),E,_),
    not attribute((encoding,scale_type),E,linear).

% @soft(only_discrete) Only discrete encoding channels are used in a mark.
preference(only_discrete,M) :-
    attribute(mark_channel_discrete_or_binned,M,_).

% @soft(multi_non_pos) Prefer not to use multiple non-positional encoding channels.
preference(multi_non_pos,M) :-
    entity(mark,_,M),
    { attribute((mark,channel),M,C): domain(non_positional,C) } > 1.

% @soft(non_pos_used_before_pos) Prefer not to use non-positional channels until all positional channels are used.
preference(non_pos_used_before_pos,M) :-
    attribute((mark,channel),M,C),
    domain(non_positional,C),
    not attribute((mark,channel),M,(x;y)).

% @soft(aggregate_group_by_raw) Aggregate plots should not use raw continuous as group by.
preference(aggregate_group_by_raw,E) :-
    entity(encoding,M,EA),
    attribute((encoding,aggregate),EA,_),
    entity(encoding,M,E),
    not attribute(mark_encoding_discrete_or_binned,M,E),
    not attribute((encoding,aggregate),E,_).

% @soft(aggregate_no_discrete) Aggregate should also have a discrete encoding to group by.
preference(aggregate_no_discrete,M) :-
    entity(encoding,M,EA),
    attribute((encoding,aggregate),EA,_),
    not attribute(mark_encoding_discrete_or_binned,M,_).

% @soft(x_y_raw) Prefer not to use plot with both x and y discrete and no aggregate as it leads to occlusion.
preference(x_y_raw,M) :-
    attribute(mark_channel_discrete_or_binned,M,x),
    attribute(mark_channel_discrete_or_binned,M,y),
    entity(encoding,M,E),
    not attribute(mark_encoding_discrete_or_binned,M,E),
    not attribute((encoding,aggregate),E,_).

% @soft(continuous_not_zero) Prefer to include zero for continuous (binned doesn't need zero).
preference(continuous_not_zero,E) :-
    not attribute(mark_encoding_discrete_or_binned,M,E),
    attribute(mark_encoding_scale,M,E,S),
    not attribute((scale,zero),S,true).

% @soft(size_not_zero) Prefer zero size (even when binned).
preference(size_not_zero,E) :-
    attribute((encoding,channel),E,size),
    attribute(mark_encoding_scale,M,E,S),
    not attribute((scale,zero),S,true).

% @soft(continuous_pos_not_zero) Prefer zero continuous positional.
preference(continuous_pos_not_zero,E) :-
    attribute((encoding,channel),E,(x;y)),
    not attribute(mark_encoding_discrete_or_binned,M,E),
    attribute(mark_encoding_scale,M,E,S),
    not attribute((scale,zero),S,true).

% @soft(skew_zero) Prefer not to use zero when the difference between min and max is smaller than distance to 0.
preference(skew_zero,E) :-
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX),
    EXT = MAX - MIN,
    |MAX| > EXT,
    |MIN| > EXT,
    entity(encoding,M,E),
    attribute((encoding,field),E,F),
    attribute(mark_encoding_scale,M,E,S),
    attribute((scale,zero),S,true).

% @soft(cross_zero) Prefer not to include zero as baseline when the range of data crosses zero.
preference(cross_zero,E) :-
    attribute((field,min),F,MIN),
    attribute((field,max),F,MAX),
    MAX > 0,
    MIN < 0,
    entity(encoding,M,E),
    attribute((encoding,field),E,F),
    attribute(mark_encoding_scale,M,E,S),
    attribute((scale,zero),S,true).

% @soft(only_y) Prefer to use only x instead of only y.
preference(only_y,M) :-
    attribute((mark,channel),M,y),
    not attribute((mark,channel),M,x).

% @soft(binned_orientation_not_x) Prefer binned quantative on x axis.
preference(binned_orientation_not_x,E) :-
    attribute((field,type),F,(number;datetime)),
    attribute((encoding,field),E,F),
    attribute((encoding,binning),E,_),
    not attribute((encoding,channel),E,x).

% @soft(high_cardinality_ordinal) Prefer not to use ordinal for fields with high cardinality.
preference(high_cardinality_ordinal,E) :-
    attribute(encoding_cardinality,E,N),
    attribute((encoding,scale_type),E,ordinal),
    N > 30.

% @soft(high_cardinality_categorical_grt10) Prefer not to use categorical (color) for fields with high cardinality.
preference(high_cardinality_categorical_grt10,E) :-
    attribute(encoding_cardinality,E,N),
    attribute((encoding,scale_type),E,categorical),
    N > 10.

% @soft(high_cardinality_shape) Prefer not to use high cardinality ordinal for shape.
preference(high_cardinality_shape,E) :-
    attribute(encoding_cardinality,E,N),
    attribute((encoding,channel),E,shape),
    N > 8.

% @soft(high_cardinality_size) Prefer not to use size when the cardinality is large on x or y.
preference(high_cardinality_size,E) :-
    attribute((mark,channel),M,size),
    entity(encoding,M,E),
    attribute(encoding_cardinality,E,N),
    attribute((encoding,channel),E,(x;y)),
    not attribute(mark_encoding_discrete_or_binned,M,E),
    N > 100.

% @soft(horizontal_scrolling_x) Avoid high cardinality on x as it causes horizontal scrolling.
preference(horizontal_scrolling_x,E) :-
    attribute((encoding,channel),E,x),
    attribute(encoding_cardinality,E,N),
    attribute(mark_encoding_discrete_or_binned,_,E),
    N > 50.

% @soft(horizontal_scrolling_col) Avoid high cardinality on column as it causes horizontal scrolling.
preference(horizontal_scrolling_col,F) :-
    attribute((facet,channel),F,col),
    attribute(facet_cardinality,F,N),
    N > 5.

% @soft(date_scale) Prefer to use linear/ordinal scale type with dates.
preference(date_scale,E) :-
    attribute((field,type),F,datetime),
    attribute((encoding,field),E,F),
    not attribute((encoding,scale_type),E,linear),
    not attribute((encoding,scale_type),E,ordinal).

% @soft(number_linear) Prefer use linear for numbers with high cardinality.
preference(number_linear,E) :-
    attribute((field,type),F,number),
    attribute((field,unique),F,N),
    N > 20,
    attribute((encoding,field),E,F),
    not attribute((encoding,binning),E,_),
    not attribute((encoding,scale_type),E,linear).

% @soft(value_agg) Prefer not to aggregate for value tasks.
preference(value_agg,V) :-
    attribute(task,root,value),
    entity(mark,V,M),
    entity(encoding,M,E),
    attribute((encoding,aggregate),E,_).

% @soft(summary_facet) Prefer not to use facet for summary tasks as it makes it difficult to compare.
preference(summary_facet,V) :-
    attribute(task,root,summary),
    entity(facet,V,_).

% @soft(c_d_col) Prefer not to use continuous on x, discrete on y, and column.
preference(c_d_col,V) :-
    entity(mark,V,M),
    not attribute(mark_channel_discrete_or_binned,M,x),
    attribute(mark_channel_discrete_or_binned,M,y),
    entity(facet,V,F),
    attribute((facet,channel),F,col).

% @soft(date_not_x) Prefer datetime on x.
preference(date_not_x,E) :-
    attribute((field,type),F,datetime),
    attribute((encoding,field),E,F),
    not attribute((encoding,channel),E,x).

% @soft(x_row) Positional interactions as suggested by Kim et al.
preference(x_row,V) :-
    entity(mark,V,M),
    attribute((mark,channel),M,x),
    entity(facet,V,F),
    attribute((facet,channel),F,row).

% @soft(y_row) Positional interactions as suggested by Kim et al.
preference(y_row,V) :-
    entity(mark,V,M),
    attribute((mark,channel),M,y),
    entity(facet,V,F),
    attribute((facet,channel),F,row).

% @soft(x_col) Positional interactions as suggested by Kim et al.
preference(x_col,V) :-
    entity(mark,V,M),
    attribute((mark,channel),M,x),
    entity(facet,V,F),
    attribute((facet,channel),F,col).

% @soft(y_col) Positional interactions as suggested by Kim et al.
preference(y_col,V) :-
    entity(mark,V,M),
    attribute((mark,channel),M,y),
    entity(facet,V,F),
    attribute((facet,channel),F,col).

% @soft(color_entropy_high) Entropy, primary quantitaty interactions as suggested by Kim et al.
preference(color_entropy_high,E) :-
    attribute((field,entropy),F,EN),
    attribute((encoding,field),E,F),
    attribute((encoding,channel),E,color),
    attribute((encoding,scale_type),E,linear),
    EN > 5000.

% @soft(color_entropy_low) Entropy, primary quantitaty interactions as suggested by Kim et al.
preference(color_entropy_low,E) :-
    attribute((field,entropy),F,EN),
    attribute((encoding,field),E,F),
    attribute((encoding,channel),E,color),
    attribute((encoding,scale_type),E,linear),
    EN <= 5000.

% @soft(size_entropy_high) Entropy, primary quantitaty interactions as suggested by Kim et al.
preference(size_entropy_high,E) :-
    attribute((field,entropy),F,EN),
    attribute((encoding,field),E,F),
    attribute((encoding,channel),E,size),
    attribute((encoding,scale_type),E,linear),
    EN > 5000.

% @soft(size_entropy_low) Entropy, primary quantitaty interactions as suggested by Kim et al.
preference(size_entropy_low,E) :-
    attribute((field,entropy),F,EN),
    attribute((encoding,field),E,F),
    attribute((encoding,channel),E,size),
    attribute((encoding,scale_type),E,linear),
    EN <= 5000.

% @soft(linear_scale) linear scale.
preference(linear_scale,E) :-
    attribute((encoding,scale_type),E,linear).

% @soft(log_scale) log scale.
preference(log_scale,E) :-
    attribute((encoding,scale_type),E,log).

% @soft(ordinal_scale) ordinal scale.
preference(ordinal_scale,E) :-
    attribute((encoding,scale_type),E,ordinal).

% @soft(categorical_scale) categorical scale.
preference(categorical_scale,E) :-
    attribute((encoding,scale_type),E,categorical).

% @soft(stack_zero) Zero base for stack op.
preference(stack_zero,E) :-
    attribute((encoding,stack),E,zero).

% @soft(stack_center) Center groupbys as stack op.
preference(stack_center,E) :-
    attribute((encoding,stack),E,center).

% @soft(stack_normalize) Normalize between groupbys as stack op.
preference(stack_normalize,E) :-
    attribute((encoding,stack),E,normalize).

% @soft(value_point) Point mark for value tasks.
preference(value_point,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,point).

% @soft(value_bar) Bar mark for value tasks.
preference(value_bar,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,bar).

% @soft(value_line) Line mark for value tasks.
preference(value_line,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,line).

% @soft(value_area) Area mark for value tasks.
preference(value_area,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,area).

% @soft(value_text) Text mark for value tasks.
preference(value_text,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,text).

% @soft(value_tick) Tick mark for value tasks.
preference(value_tick,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,tick).

% @soft(value_rect) Rect mark for value tasks.
preference(value_rect,M) :-
    attribute(task,root,value),
    attribute((mark,type),M,rect).

% @soft(summary_point) Point mark for summary tasks.
preference(summary_point,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,point).

% @soft(summary_bar) Bar mark for summary tasks.
preference(summary_bar,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,bar).

% @soft(summary_line) Line mark for summary tasks.
preference(summary_line,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,line).

% @soft(summary_area) Area mark for summary tasks.
preference(summary_area,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,area).

% @soft(summary_text) Text mark for summary tasks.
preference(summary_text,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,text).

% @soft(summary_tick) Tick mark for summary tasks.
preference(summary_tick,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,tick).

% @soft(summary_rect) Rect mark for summary tasks.
preference(summary_rect,M) :-
    attribute(task,root,summary),
    attribute((mark,type),M,rect).
