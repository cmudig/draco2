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
