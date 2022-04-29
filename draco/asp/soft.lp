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

% @soft(x_y_raw) Prefer not to use plot with x and y discrete and no aggregate as it leads to occlusion.
preference(x_y_raw,M) :-
    attribute(mark_channel_discrete_or_binned,M,(x;y)),
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
