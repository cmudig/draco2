% ====== Definitions of valid function domains ======

% @definition(mark_type) Types of marks to encode data.
domain((mark,type),(point;bar;line;area;text;tick;rect)).

% @definition(field_type) Basic types of the data.
domain((field,type),(string;number;boolean;datetime)).

% @definition(aggregate) Aggregation functions.
domain((encoding,aggregate),(count;mean;median;min;max;stdev;sum)).
domain(summative_aggregate,(count;sum)).

% @definition(binning) Numbers of bins that can be recommended, any natural number is allowed.
domain((encoding,binning),(10;25;200)).

% @definition(channel) Encoding channels.
domain(single_channel,(x;y;color;size;shape;text;row;column)).
domain(multi_channel,detail).
domain(channel,C) :- domain(single_channel,C).
domain(channel,C) :- domain(multi_channel,C).
domain(non_positional,(color;size;shape;text;detail)).

domain((encoding,channel),C) :- domain(channel,C).
domain((scale,channel),C) :- domain(channel,C).

% @definition(scale_type) Scale types.
domain((scale,type),(linear;log;ordinal)).

% @definition(task) Tasks.
domain(task,(value;summary)).

% @definition(stack) Stacking methods.
domain(stack,(zero;normalize)).
