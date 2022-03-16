% ====== Definitions of valid function domains ======

% @definition(mark_type) Types of marks to encode data.
domain((mark,type),(point;bar;line;area;text;tick;rect)).

% @definition(field_type) Basic types of the data.
domain((field,type),(string;number;boolean;datetime)).

% @definition(field_names) Basic types of the data.
domain((field,name),F) :- attribute((field,name),_,F).

% @definition(field_ids)
domain((encoding,field),F) :- entity(field,_,F).

% @definition(aggregate) Aggregation functions.
domain((encoding,aggregate),(count;mean;median;min;max;stdev;sum)).
domain((encoding,aggregate),(count;sum)).

% @definition(binning) Numbers of bins that can be recommended, any natural number is allowed.
domain((encoding,binning),(10;25;200)).

% @definition(channel) Encoding channels.
domain(positional,(x;y)).
domain(non_positional,(color;size;shape;text;detail)).
domain(single_channel,C) :- domain(positional,C).
domain(single_channel,C) :- domain(non_positional,C).
domain(multi_channel,detail).
domain(channel,C) :- domain(single_channel,C).
domain(channel,C) :- domain(multi_channel,C).

domain((encoding,channel),C) :- domain(channel,C).
domain((scale,channel),C) :- domain(channel,C).

% @definition(scale_type) Scale types.
domain(discrete_scale,(ordinal;categorical)).
domain(continuous_scale,(log;linear)).
domain(scale_type,T) :- domain(discrete_scale,T).
domain(scale_type,T) :- domain(continuous_scale,T).

domain((scale,type),T) :- domain(scale_type,T).

% @definition(task) Tasks.
domain(task,(value;summary)).

% @definition(stack) Stacking methods.
domain((encoding,stack),(zero;center;normalize)).

% @definition(scale_zero) Scale start with 0.
domain((scale,zero),true).

% @definition(facets) Definition for facets
domain((facet,field),F) :- entity(field,_,F).

domain(facet_channel,(row;col)).
domain((facet,channel),C) :- domain(facet_channel,C).

domain((facet,binning),(10;25;200)).

