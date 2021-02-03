% ====== Definitions of valid function domains ======

% @definition(mark_type) Types of marks to encode data.
domain(mark_type,(point;bar;line;area;text;tick;rect)).

% @definition(field_type) Basic types of the data.
domain(field_type,(string;number;boolean;datetime)).

% @definition(aggregate) Supported aggregation functions.
domain(aggregate,(count;mean;median;min;max;stdev;sum)).
domain(summative_aggregate,(count;sum)).

% @definition(binning) Numbers of bins that can be recommended, any natural number is allowed.
domain(binning,(10;25;200)).

% @definition(channel) Encoding channels.
domain(single_channel,(x;y;color;size;shape;text;row;column)).
domain(multi_channel,detail).
domain(channel,C) :- domain(single_channel,C).
domain(channel,C) :- domain(multi_channel,C).
domain(non_positional,(color;size;shape;text;detail)).

% @definition(task) Possible tasks.
domain(task,(value;summary)).

% @definition(stack) Possible stacking methods.
domain(stack,(zero;normalize)).
