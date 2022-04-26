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

% @soft(shape_high_cardinality) Shape channel should not have too high cardinality.
preference(shape_high_cardinality,E) :-
    attribute((encoding,channel),E,shape),
    attribute(encoding_cardinality,E,N),
    N > 5.

% @soft(number_categorical) Should not use categorical scale for number field.
preference(number_categorical,M,F,C) :-
    attribute((field,type),F,number),
    attribute(mark_channel_field,M,C,F),
    attribute(mark_scale_channel,M,categorical,C).

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

% @soft(high_cardinality_categorical_grt20) Prefer not to use categorical (color) for fields with high cardinality.
preference(high_cardinality_categorical_grt20,E) :-
    attribute(encoding_cardinality,E,N),
    attribute((encoding,scale_type),E,categorical),
    N > 20.

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
    N > 50.

% @soft(horizontal_scrolling_col) Avoid high cardinality on column as it causes horizontal scrolling.
preference(horizontal_scrolling_col,F) :-
    attribute((facet,channel),F,col),
    attribute(facet_cardinality,F,N),
    N > 5.

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
